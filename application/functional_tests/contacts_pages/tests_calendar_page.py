import datetime
import json
from selenium.webdriver.common.keys import Keys
from django.test import Client
from django.contrib.auth import get_user_model
from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time
from contacts_app.models import Contact, Network, Party, Event
from django.db.models.functions import Lower
#from seleniumlogin import force_login # c'est nécessaire pour le login par selenium


class Test0CalendarPage(LiveServerTestCase):

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

        # créer un Event
        self.event1 = Event.objects.create(
            Text = 'Search Milk 14h', 
            Date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 18),
            fk_user = self.user1
        )
        self.day = self.event1.Date.day
        self.task = self.event1.Text

    def test_calendar_page(self):
            
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

        # accéder à la page calendar
        self.browser.find_element('id', 'calendar').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.calendar_url)
        self.assertIn('number of events:', self.browser.find_element('id', 'count_events').text)
        time.sleep(1)

        # Vérifier l'interface de l'en-tête
        text = self.browser.find_element('tag name', 'h1').text
        self.assertEqual(text, 'Contacts Booklet')
        nav = self.browser.find_element('class name', 'navigation')
        self.assertEqual(nav.find_element('id', 'span_menu').text, 'menu:')
        self.assertEqual(nav.find_element('id', 'contacts').text, 'contacts')
        self.assertEqual(nav.find_element('id', 'networks').text, 'networks')
        self.assertEqual(nav.find_element('id', 'parties').text, 'parties')
        self.assertEqual(nav.find_element('id', 'calendar').text, 'calendar')
        self.assertEqual(nav.find_element('id', 'log').text, 'log out')

        # Vérifier l'interface de l'étiquette du calendrier
        self.assertEqual(self.browser.find_elements('tag name', 'button')[0].text, '<')
        self.assertEqual(self.browser.find_elements('tag name', 'button')[1].text, '>')
        text = datetime.datetime.now().strftime('%B %Y')
        self.assertEqual(self.browser.find_element('id', 'date').text, text)
        text = 'number of events: ' + str(1)
        self.assertEqual(self.browser.find_element('id', 'count_events').text, text)
        self.assertEqual(self.browser.find_element('id', 'page_numero').text, '')

        # Vérifier la structure du calendrier
        table = self.browser.find_element('tag name', 'table')
        th_list = table.find_elements('tag name', 'th')
        check_title_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in range(len(check_title_list)):
            if(th_list[i].text != check_title_list[i]):
                self.assertEqual(False, True)
        self.assertEqual(True, True)
        tbody = self.browser.find_element('tag name', 'tbody')
        self.assertEqual(len(tbody.find_elements('tag name', 'tr')), 6)

        # Récupérer la case du calendrier possèdant une tâche
        liste1 = self.browser.find_elements('tag name', 'td')
        indice = 0
        for i in range(len(liste1)):
            if(liste1[i].find_element('tag name', 'span').text == str(self.day)):
                indice = i
                break
        
        # Vérifier la mise en forme du numéro dans la case
        text = liste1[indice].find_element('tag name', 'span').get_attribute('class')
        self.assertEqual(text, 'numero day_with_task') # vérifier visuellement

        # Vérifier la présence du texte dans la case
        text = liste1[indice].find_element('tag name', 'div').text
        self.assertEqual(text, self.task) # vérifier visuellement

        # Clique sur le bouton précèdent ("<")
        self.browser.find_elements('tag name', 'button')[0].click()
        date = datetime.datetime.now()
        date = datetime.date(date.year, date.month-1, 1)
        self.assertEqual(self.browser.find_element('id', 'date').text, date.strftime('%B %Y'))
        time.sleep(1)

        # vérifier le fonctionnement du bouton suivant (">")
        for i in range(0, 7):
            self.browser.find_elements('tag name', 'button')[1].click()
            date = datetime.date(date.year, date.month+1, 1)
            self.assertEqual(self.browser.find_element('id', 'date').text, date.strftime('%B %Y'))
            time.sleep(1)
        self.browser.find_elements('tag name', 'button')[1].click()
        self.assertEqual(self.browser.find_element('id', 'date').text, date.strftime('%B %Y'))
        time.sleep(1)
        
        # vérifier le fonctionnement du bouton précèdent ("<")
        for i in range(0, 7):
            self.browser.find_elements('tag name', 'button')[0].click()
            date = datetime.date(date.year, date.month-1, 1)
            self.assertEqual(self.browser.find_element('id', 'date').text, date.strftime('%B %Y'))
            time.sleep(1)
        self.browser.find_elements('tag name', 'button')[0].click()
        self.assertEqual(self.browser.find_element('id', 'date').text, date.strftime('%B %Y'))
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()



