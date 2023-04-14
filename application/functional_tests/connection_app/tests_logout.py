from django.test import Client
from selenium import webdriver
from connection_app.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time


class Test0Logout(LiveServerTestCase):

    # mettre en place les urls
    def setUp(self):
        #self.browser =  webdriver.Edge('functional_tests/msedgedriver.exe')
        self.browser =  webdriver.Chrome('functional_tests/chromedriver.exe')
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.contacts_url = reverse('contacts')

        # créer un User
        self.client = Client()
        User.objects.create_user(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )
    
    def test_logout(self):

        # ouverture de l'application
        self.browser.get(self.live_server_url)
        time.sleep(1)

        # se connecter et accéder à la page contacts
        self.browser.find_elements('tag name', 'input')[0].send_keys('user1')
        self.browser.find_elements('tag name', 'input')[1].send_keys('password1')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'count_contacts').text
        self.assertIn('number of contacts:', text)
        time.sleep(1)

        # se déconnecter
        self.browser.find_element('id', 'log').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        text = self.browser.find_element('tag name', 'button').text
        self.assertEqual(text, 'Log in')
        time.sleep(1)

        # tenter de retourner sur la page
        self.browser.get(self.live_server_url + self.contacts_url)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/?next=' + self.contacts_url)
        text = self.browser.find_element('tag name', 'button').text
        self.assertEqual(text, 'Log in')
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()



