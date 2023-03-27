from django.test import Client
from selenium import webdriver
from connection_app.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time


class Test0UserLogin(LiveServerTestCase):

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
        text = self.browser.find_element('tag name', 'h1').text
        self.assertEqual(text, 'Contacts Booklet')
        text = self.browser.find_elements('tag name', 'label')[0].text
        self.assertEqual(text, 'User name:')
        text = self.browser.find_elements('tag name', 'label')[1].text
        self.assertEqual(text, 'Password:')
        text = self.browser.find_elements('tag name', 'input')[0].text
        self.assertEqual(text, '')
        text = self.browser.find_elements('tag name', 'input')[1].text
        self.assertEqual(text, '')
        text = self.browser.find_element('tag name', 'button').text
        self.assertEqual(text, 'Log in')
        text = self.browser.find_elements('tag name', 'a')[0].text
        self.assertEqual(text, 'Sign-up now !')
        text = self.browser.find_elements('tag name', 'a')[1].text
        self.assertEqual(text, 'Reset the password !')
        time.sleep(1)

        # vérifier le fonctionnement du lien vers la page d'inscription
        self.browser.find_elements('tag name', 'a')[0].click()
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual('Registration', text)
        time.sleep(1)
        self.browser.get(self.live_server_url)
        time.sleep(1)

        # vérifier le fonctionnement du lien vers la page pour réinitaliser le mot de passe
        self.browser.find_elements('tag name', 'a')[1].click()
        div = self.browser.find_element('id', 'main')
        text = div.find_element('tag name', 'h1').text
        self.assertEqual('Password reset', text)
        time.sleep(1)
        self.browser.get(self.live_server_url)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides
        self.browser.find_elements('tag name', 'input')[0].send_keys('no valid user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[0].clear()
        self.browser.find_elements('tag name', 'input')[1].send_keys('no valid password')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[0].send_keys('no valid user')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        text = self.browser.find_element('id', 'message').text
        self.assertEqual(text, 'Identifiants invalides.')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données valides
        self.browser.find_elements('tag name', 'input')[0].clear()
        self.browser.find_elements('tag name', 'input')[0].send_keys('user1')
        self.browser.find_elements('tag name', 'input')[1].clear()
        self.browser.find_elements('tag name', 'input')[1].send_keys('password1')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()
    

    # test de la fonctionnalité d'inscription
    def test_signup_page(self):

        # ouverture de l'application
        self.browser.get(self.live_server_url)
        time.sleep(1)

        # redirection vers la page d'inscription
        self.browser.find_elements('tag name', 'a')[0].click()

        # vérifier l'interface de la page signUp
        text = self.browser.find_element('tag name', 'h1').text
        self.assertEqual(text, 'Contacts Booklet')
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Registration')
        text = self.browser.find_element('id', 'back').text
        self.assertEqual(text, 'back')
        text = self.browser.find_elements('tag name', 'label')[0].text
        self.assertEqual(text, 'Username:')
        text = self.browser.find_elements('tag name', 'label')[1].text
        self.assertEqual(text, 'Email:')
        text = self.browser.find_elements('tag name', 'label')[2].text
        self.assertEqual(text, 'First name:')
        text = self.browser.find_elements('tag name', 'label')[3].text
        self.assertEqual(text, 'Last name:')
        text = self.browser.find_elements('tag name', 'label')[4].text
        self.assertEqual(text, 'Password:')
        text = self.browser.find_elements('tag name', 'label')[5].text
        self.assertEqual(text, 'Password confirmation:')
        text = self.browser.find_elements('tag name', 'li')[0].text
        self.assertEqual(text, 'Your password must contain at least 8 characters.')
        text = self.browser.find_elements('tag name', 'li')[1].text
        self.assertEqual(text, 'Your password can’t be entirely numeric.')
        text = self.browser.find_elements('class name', 'helptext')[1].text
        self.assertEqual(text, 'Enter the same password as before, for verification.')
        time.sleep(1)

        # vérifier le fonctionnement bouton back
        self.browser.find_element('id', 'back').click()
        self.assertEqual(self.browser.current_url[:-1], self.live_server_url)
        text = self.browser.find_element('tag name', 'button').text
        self.assertEqual(text, 'Log in')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides --> champs requis vides
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        time.sleep(1)
        
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[1].send_keys('valid@email.com')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Registration')
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides --> valeurs des champs incorrect
        self.browser.find_elements('tag name', 'input')[5].send_keys('other_valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.signup_url)
        ul = self.browser.find_element('class name', 'errorlist')
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'The two password fields didn’t match.')
        time.sleep(1)

        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('email.com')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
        self.browser.find_elements('tag name', 'input')[5].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        ul = self.browser.find_element('class name', 'errorlist')
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'Enter a valid email address.')
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[1].clear()
        self.browser.find_elements('tag name', 'input')[1].send_keys('email@no_valid')
        self.browser.find_elements('tag name', 'input')[4].send_keys('valid_1234_password')
        self.browser.find_elements('tag name', 'input')[5].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        ul = self.browser.find_element('class name', 'errorlist')
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'Enter a valid email address.')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides --> mot de passe non valide
        self.browser.get(self.live_server_url + self.signup_url)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('valid@email.fr')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid_first_name')
        self.browser.find_elements('tag name', 'input')[3].send_keys('valid_last_name')
        self.browser.find_elements('tag name', 'input')[4].send_keys('short')
        self.browser.find_elements('tag name', 'input')[5].send_keys('short')
        self.browser.find_element('tag name', 'button').click()
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        ul = self.browser.find_element('class name', 'errorlist')
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'This password is too short. It must contain at least 8 characters.')
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[4].send_keys('12345678')
        self.browser.find_elements('tag name', 'input')[5].send_keys('12345678')
        self.browser.find_element('tag name', 'button').click()
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        ul = self.browser.find_element('class name', 'errorlist')
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'This password is entirely numeric.')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides --> le nom utilisateur existe déjà
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
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'A user with that username already exists.')
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
        text = self.browser.find_element('tag name', 'button').text
        self.assertEqual(text, 'Log in')
        time.sleep(1)

        # vérifier que le User a été crée
        self.browser.find_elements('tag name', 'input')[0].send_keys('valid_user')
        self.browser.find_elements('tag name', 'input')[1].send_keys('valid_1234_password')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()


