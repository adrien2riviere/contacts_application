from django.test import Client
from django.contrib.auth import get_user_model
from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time
#from seleniumlogin import force_login # c'est nécessaire pour le login par selenium


class Test0NavigationPage(LiveServerTestCase):

    # mettre en place les urls
    def setUp(self):
        #self.browser =  webdriver.Edge('functional_tests/msedgedriver.exe')
        self.browser =  webdriver.Chrome('functional_tests/chromedriver.exe')
        self.contacts_url = reverse('contacts')
        self.networks_url = reverse('networks')
        self.parties_url = reverse('parties')
        self.calendar_url = reverse('calendar', kwargs={'page' : 1,})

        # créer un User
        self.client = Client()
        self.user1 = get_user_model().objects.create_user(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )

    def test_navigation_bar(self):

        # ouverture de l'application
        self.browser.get(self.live_server_url)
        time.sleep(1)

         # se connecter et accéder à la page contacts
        self.browser.find_elements('tag name', 'input')[0].send_keys('user1')
        self.browser.find_elements('tag name', 'input')[1].send_keys('password1')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        self.assertIn('number of contacts:', self.browser.find_element('id', 'count_contacts').text)
        time.sleep(1)

        # Tester la barre de navigation
        liste1 = ['networks', 'parties', 'calendar', 'contacts']
        liste2 = ['number of networks:', 'number of parties:', 'number of events:', 'number of contacts:']
        liste3 = [self.networks_url, self.parties_url, self.calendar_url, self.contacts_url]
        liste4 = ['count_networks', 'count_parties', 'count_events', 'count_contacts']
        for i in range(len(liste1)):
            self.browser.find_element('id', liste1[i]).click()
            self.assertEqual(self.browser.current_url, self.live_server_url + liste3[i])
            self.assertIn(liste2[i], self.browser.find_element('id', liste4[i]).text)
            time.sleep(1)

        # Vérifier la redirection lors d'un clique sur "log out"
        self.browser.find_element('id', 'log').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        text = self.browser.find_element('tag name', 'button').text
        self.assertEqual(text, 'Log in')
        time.sleep(1)