from django.test import Client
from selenium import webdriver
from connection_app.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time


class Test0SignUp(LiveServerTestCase):

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

    # test de la fonctionnalité d'inscription
    def test_signup_page(self):

        # ouverture de l'application
        self.browser.get(self.live_server_url)
        time.sleep(1)

        # redirection vers la page d'inscription
        self.browser.find_elements('tag name', 'a')[0].click()

        # vérifier l'interface de la page signUp
        self.assertEqual(self.browser.find_element('tag name', 'h1').text, 'Contacts Booklet')
        self.assertEqual(self.browser.find_element('tag name', 'h2').text, 'Registration')
        self.assertEqual(self.browser.find_element('id', 'back').text, 'back')
        liste1 = ['Username:', 'Email:', 'First name:', 'Last name:', 'Password:', 'Password confirmation:']
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('tag name', 'label')[i].text, liste1[i])
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('tag name', 'input')[i].text, '')
        text = 'Your password must contain at least 8 characters.'
        self.assertEqual(self.browser.find_elements('tag name', 'li')[0].text, text)
        text = 'Your password can’t be entirely numeric.'
        self.assertEqual(self.browser.find_elements('tag name', 'li')[1].text, text)
        text = 'Enter the same password as before, for verification.'
        self.assertEqual(self.browser.find_elements('class name', 'helptext')[1].text, text)
        time.sleep(1)

        # vérifier le fonctionnement bouton back
        self.browser.find_element('id', 'back').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        self.assertEqual(self.browser.find_element('tag name', 'button').text, 'Log in')
        time.sleep(1)

        # retour sur la page signup
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)

        # vérifier la limitation des champs en nombre de caractères
        text = 'a_very_long_entry_with_more_than_thirty_or_fifty_characters'
        liste1 = [text[:30], text[:40], text[:30], text[:30], text[:50], text[:50]]
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[i].send_keys(text)
            self.assertEqual(self.browser.find_elements('tag name', 'input')[i].get_attribute('value'), liste1[i])
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des champs requis vides
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        time.sleep(1)
        liste1 = ['valid_user', 'valid@email.com', 'valid_first_name', 'valid_last_name', 'valid_1234_password']
        liste2 = self.browser.find_elements('tag name', 'input')
        for i in range(len(liste1)):
            liste2[i].send_keys(liste1[i])
            self.browser.find_element('tag name', 'button').click()
            self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
            time.sleep(1)

        # vérifier le fonctionnement du formulaire pour une différence entre password et password confirmation
        self.browser.find_elements('tag name', 'input')[5].send_keys('other_valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        ul = self.browser.find_element('class name', 'errorlist')
        text = 'The two password fields didn’t match.'
        self.assertEqual(ul.find_element('tag name', 'li').text, text)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour un email incorrect
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('email')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
        self.browser.find_elements('tag name', 'input')[5].send_keys('valid_1234_password')
        time.sleep(1)
        liste1 = ['email', 'email.com', 'email@no_valid']
        for i in range(len(liste1)):
            if(i>0):
                self.browser.find_elements('tag name', 'input')[1].clear()
                time.sleep(1)
                self.browser.find_elements('tag name', 'input')[1].send_keys(liste1[i])
                self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
                self.browser.find_elements('tag name', 'input')[5].send_keys('valid_1234_password') 
                time.sleep(1)
            self.browser.find_element('tag name', 'button').click()
            ul = self.browser.find_element('class name', 'errorlist')
            text = 'Enter a valid email address.'
            self.assertEqual(ul.find_element('tag name', 'li').text, text)
            time.sleep(1)

        # vérifier le fonctionnement du formulaire pour un mot de passe non valide
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('valid@email.fr')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        time.sleep(1)
        liste1 = ['short', '12345678']
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[4].send_keys(liste1[i])
            self.browser.find_elements('tag name', 'input')[5].send_keys(liste1[i])
            time.sleep(1)
            self.browser.find_element('tag name', 'button').click()
            ul = self.browser.find_element('class name', 'errorlist')
            if(liste1[i] == 'short'):
                text = 'This password is too short. It must contain at least 8 characters.'
            elif(liste1[i] == '12345678'):
                text = 'This password is entirely numeric.'
            self.assertEqual(ul.find_element('tag name', 'li').text, text)
            time.sleep(1)

        # vérifier le fonctionnement du formulaire pour un nom utilisateur déjà existant
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('user1')
        self.browser.find_elements('tag name', 'input')[1].send_keys('valid@email.fr')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
        self.browser.find_elements('tag name', 'input')[5].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        ul = self.browser.find_element('class name', 'errorlist')
        text = 'A user with that username already exists.'
        self.assertEqual(ul.find_element('tag name', 'li').text, text)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données valides
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('valid@email.fr')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
        self.browser.find_elements('tag name', 'input')[5].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        self.assertEqual(self.browser.find_element('tag name', 'button').text, 'Log in')
        time.sleep(1)

        # vérifier que le User a été crée
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        self.assertIn('number of contacts: ', self.browser.find_element('id', 'count_contacts').text)
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()