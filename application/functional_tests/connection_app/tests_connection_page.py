from django.test import Client
from selenium import webdriver
from connection_app.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time


class Test0Login(LiveServerTestCase):

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
    
    # test de la fonctionnalité de connexion
    def test_login_page(self):

        # ouverture de l'application
        self.browser.get(self.live_server_url)

        # vérifier l'interface de la page login
        self.assertEqual(self.browser.find_element('tag name', 'h1').text, 'Contacts Booklet')
        self.assertEqual(self.browser.find_elements('tag name', 'label')[0].text, 'User name:')
        self.assertEqual(self.browser.find_elements('tag name', 'label')[1].text, 'Password:')
        self.assertEqual(self.browser.find_elements('tag name', 'input')[0].text, '')
        self.assertEqual(self.browser.find_elements('tag name', 'input')[1].text, '')
        self.assertEqual(self.browser.find_element('tag name', 'button').text, 'Log in')
        self.assertEqual(self.browser.find_elements('tag name', 'a')[0].text, 'Sign-up now !')
        self.assertEqual(self.browser.find_elements('tag name', 'a')[1].text, 'Reset the password !')
        time.sleep(1)

        # vérifier le fonctionnement du lien vers la page d'inscription
        self.browser.find_elements('tag name', 'a')[0].click()
        self.assertEqual('Registration', self.browser.find_element('tag name', 'h2').text)
        time.sleep(1)

        # vérifier le fonctionnement du lien vers la page pour réinitaliser le mot de passe
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'a')[1].click()
        div = self.browser.find_element('id', 'main')
        self.assertEqual('Password reset', div.find_element('tag name', 'h1').text)
        time.sleep(1)

        # vérifier la limitation des champs en nombre de caractères
        self.browser.get(self.live_server_url)
        time.sleep(1)
        text = 'a_very_long_entry_with_more_than_thirty_or_fifty_characters'
        liste1 = [text[:30], text[:50]]
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[i].send_keys(text)
            self.assertEqual(self.browser.find_elements('tag name', 'input')[i].get_attribute('value'), liste1[i])
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour un password vide
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('no valid user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour un username vide
        self.browser.find_elements('tag name', 'input')[0].clear()
        self.browser.find_elements('tag name', 'input')[1].send_keys('no valid password')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour un utilisateur inexistant
        self.browser.find_elements('tag name', 'input')[0].send_keys('no valid user')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        self.assertEqual(self.browser.find_element('id', 'message').text, 'Identifiants invalides.')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données valides
        self.browser.find_elements('tag name', 'input')[0].clear()
        self.browser.find_elements('tag name', 'input')[0].send_keys('user1')
        self.browser.find_elements('tag name', 'input')[1].clear()
        self.browser.find_elements('tag name', 'input')[1].send_keys('password1')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        self.assertIn('number of contacts:', self.browser.find_element('id', 'count_contacts').text)
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()