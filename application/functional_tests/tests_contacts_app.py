import os
from django.test import Client
from django.contrib.auth import get_user_model
from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time
from contacts_app.models import Contact


class Test0Contact(LiveServerTestCase):

    # mettre en place les urls
    def setUp(self):
        #self.browser =  webdriver.Edge('functional_tests/msedgedriver.exe')
        self.browser =  webdriver.Chrome('functional_tests/chromedriver.exe')
        self.contacts_url = reverse('contacts')
        self.add_contact_url = reverse('addContact')

        # utiliser des images pour les tests
        self.src_no_image = '/image/image/no-image.png'
        self.src_image_tests = '/image/image/image_tests.jpg'
        self.src_image_tests_remove = '/image/image_tests.jpg'

        # créer un User
        self.client = Client()
        self.user1 = get_user_model().objects.create_user(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )
    
    # test de la fonctionnalité d'ajout de contact
    def test_add_contact_page(self):

        # ouverture de l'application
        self.browser.get(self.live_server_url)
        time.sleep(1)

        # se connecter et accéder à la page contacts
        self.browser.find_elements('tag name', 'input')[0].send_keys('user1')
        self.browser.find_elements('tag name', 'input')[1].send_keys('password1')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)

        # accéder à la page addContact
        self.browser.find_element('id', 'add_btn').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Add a contact')
        time.sleep(1)

        # vérifier l'interface de la page addContact
        text = self.browser.find_element('tag name', 'h1').text
        self.assertEqual(text, 'Contacts Booklet')
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Add a contact')
        text = self.browser.find_element('tag name', 'img').get_attribute('src')
        self.assertEqual(text, self.live_server_url + '/image/image/no-image.png')
        text = self.browser.find_elements('tag name', 'label')[0].text
        self.assertEqual(text, 'First name:')
        text = self.browser.find_elements('tag name', 'label')[1].text
        self.assertEqual(text, 'Last name:')
        text = self.browser.find_elements('tag name', 'label')[2].text
        self.assertEqual(text, 'E-mail:')
        text = self.browser.find_elements('tag name', 'label')[3].text
        self.assertEqual(text, 'Telephone n°1:')
        text = self.browser.find_elements('tag name', 'label')[4].text
        self.assertEqual(text, 'Telephone n°2:')
        text = self.browser.find_elements('tag name', 'label')[5].text
        self.assertEqual(text, 'Picture:')

        # vérifier le fonctionnement bouton back
        self.browser.find_element('tag name', 'a').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données non valides
        self.browser.get(self.live_server_url + self.add_contact_url)
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[0].send_keys('first_name')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[0].clear()
        self.browser.find_elements('tag name', 'input')[1].send_keys('last_name')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[0].send_keys('first_name')
        self.browser.find_elements('tag name', 'input')[2].send_keys('email')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[2].clear()
        self.browser.find_elements('tag name', 'input')[2].send_keys('email.fr')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        time.sleep(1)

        self.browser.find_elements('tag name', 'input')[2].clear()
        self.browser.find_elements('tag name', 'input')[2].send_keys('no_valid@email')
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        ul = self.browser.find_element('class name', 'errorlist')
        text = ul.find_element('tag name', 'li').text
        self.assertEqual(text, 'Enter a valid email address.')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données valides minimales
        self.browser.find_elements('tag name', 'input')[2].clear()
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)

        # vérifier l'ajout du contact
        self.browser.find_element('tag name', 'input').send_keys('first_name')
        tbody = self.browser.find_element('tag name', 'tbody')
        tr_contacts = tbody.find_elements('tag name', 'tr')
        is_find = False
        for i in range(len(tr_contacts)):
            tr_contact = tr_contacts[i]
            td_contacts = tr_contact.find_elements('tag name', 'td')
            text = td_contacts[0].text
            if(text == 'first_name'):
                text = td_contacts[1].text
            if(text == 'last_name'):
                is_find = True
                break
        self.assertEqual(True, is_find)
        time.sleep(1)

        # vérifier les données du contact qui a été ajouté
        td_buttons = tr_contact.find_elements('tag name', 'td')[-1]
        td_buttons.find_elements('tag name', 'button')[0].click()
        id = Contact.objects.filter(fk_user = self.user1, first_name = 'first_name', last_name = 'last_name')[0].id
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('contactDetails', kwargs={'id': id,}))
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Contact details')
        text = self.browser.find_elements('class name', 'info')[0].text
        self.assertEqual(text, 'first_name')
        text = self.browser.find_elements('class name', 'info')[1].text
        self.assertEqual(text, 'last_name')
        text = self.browser.find_elements('class name', 'info')[2].text
        self.assertEqual(text, '')
        text = self.browser.find_elements('class name', 'info')[3].text
        self.assertEqual(text, '')
        text = self.browser.find_elements('class name', 'info')[4].text
        self.assertEqual(text, '')
        text = self.browser.find_element('tag name', 'img').get_attribute('src')
        self.assertEqual(text, self.live_server_url + self.src_no_image)
        time.sleep(1)

        # retour sur la page Addcontact
        self.browser.get(self.live_server_url + self.contacts_url)
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)
        self.browser.find_element('id', 'add_btn').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.add_contact_url)
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Add a contact')
        time.sleep(1)

        # vérifier le fonctionnement du formulaire pour des données valides et complètes
        self.browser.find_elements('tag name', 'input')[0].send_keys('first_name_bis')
        self.browser.find_elements('tag name', 'input')[1].send_keys('last_name_bis')
        self.browser.find_elements('tag name', 'input')[2].send_keys('valid@email.com')
        self.browser.find_elements('tag name', 'input')[3].send_keys('06 00 00 00 01')
        self.browser.find_elements('tag name', 'input')[4].send_keys('02 00 00 00 01')
        self.browser.find_elements('tag name', 'input')[5].send_keys('C:/Users/adriv/Documents/application_rncp/application/functional_tests/image_tests.jpg')
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        text = self.browser.find_element('id', 'contacts').text
        self.assertEqual(text, 'contacts')
        time.sleep(1)

        # vérifier l'ajout du contact
        self.browser.find_element('tag name', 'input').send_keys('first_name_bis')
        tbody = self.browser.find_element('tag name', 'tbody')
        tr_contacts = tbody.find_elements('tag name', 'tr')
        is_find = False
        for i in range(len(tr_contacts)):
            tr_contact = tr_contacts[i]
            td_contacts = tr_contact.find_elements('tag name', 'td')
            text = td_contacts[0].text
            if(text == 'first_name_bis'):
                text = td_contacts[1].text
            if(text == 'last_name_bis'):
                is_find = True
                break
        self.assertEqual(True, is_find)
        time.sleep(1)
        
        # vérifier les données du contact qui a été ajouté
        td_buttons = tr_contact.find_elements('tag name', 'td')[-1]
        td_buttons.find_elements('tag name', 'button')[0].click()
        id = Contact.objects.filter(fk_user = self.user1, first_name = 'first_name_bis', last_name = 'last_name_bis')[0].id
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('contactDetails', kwargs={'id': id,}))
        text = self.browser.find_element('tag name', 'h2').text
        self.assertEqual(text, 'Contact details')
        text = self.browser.find_elements('class name', 'info')[0].text
        self.assertEqual(text, 'first_name_bis')
        text = self.browser.find_elements('class name', 'info')[1].text
        self.assertEqual(text, 'last_name_bis')
        text = self.browser.find_elements('class name', 'info')[2].text
        self.assertEqual(text, 'valid@email.com')
        text = self.browser.find_elements('class name', 'info')[3].text
        self.assertEqual(text, '06 00 00 00 01')
        text = self.browser.find_elements('class name', 'info')[4].text
        self.assertEqual(text, '02 00 00 00 01')
        text = self.browser.find_element('tag name', 'img').get_attribute('src')
        self.assertEqual(text, self.live_server_url + self.src_image_tests)
        time.sleep(1)

        # supprimer l'image
        os.remove('C:/Users/adriv/Documents/application_rncp/application' + self.src_image_tests_remove)
        
        # fermeture de l'application à la fin des tests
        self.browser.close()