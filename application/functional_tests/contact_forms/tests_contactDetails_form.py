import json
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
        self.contact_details_url = reverse('contactDetails', kwargs={'id' : 2})

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

        self.count_contacts = 5

        # créer les chaines de texte pour la page contact details
        self.first_name = 'Aurelie'
        self.last_name = 'LXXXXX'
        self.email = 'axxxxx@live.fr'
        self.telephone1 = '06 00 00 00 01'
        self.telephone2 = '02 00 00 00 01'

    # test de la fonctionnalité details d'un contact
    def test_contact_details_page(self):

        # chargement des données de contacts
        file = open("./functional_tests/json_datas.json")
        datas = json.load(file)

        # créations des contacts de user1
        for i in range(self.count_contacts):
            c_json = datas["Contacts"][i]
            Contact.objects.create(id = c_json["id"], first_name = c_json["first_name"], last_name = c_json["last_name"], 
            email = c_json["email"], telephone1 = c_json["telephone1"], telephone2 = c_json["telephone2"], 
            profile_photo = c_json["profile_photo"], fk_user = self.user1)
        
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

        # selectionner la ligne désiré
        tbody = self.browser.find_element('tag name', 'tbody')
        tr1 = tbody.find_elements('tag name', 'tr')[1]
        tr1.click() # la ligne devient grise et foncée
        time.sleep(1)

        # accéder à la page des détails du contact
        td1 = tr1.find_elements('tag name', 'td')[-1]
        button1 = td1.find_elements('tag name', 'button')[0]
        button1.click()
        time.sleep(1)
        
        # vérifier l'interface de la page de détails du contact
        self.assertEqual(self.browser.find_element('tag name', 'h1').text, 'Contacts Booklet')
        self.assertEqual(self.browser.find_element('tag name', 'h2').text, 'Contact details')
        text = self.live_server_url + '/image/image/no-image.png'
        self.assertEqual(self.browser.find_element('tag name', 'img').get_attribute('src'), text)
        liste1 = ['First name:', 'Last name:', 'E-mail:', 'Telephone n°1:', 'Telephone n°2:']
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('tag name', 'label')[i].text, liste1[i])

        # vérifier les informations de la page de détails du contact
        liste1 = [self.first_name, self.last_name, self.email, self.telephone1, self.telephone2]
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('class name', 'info')[i].text, liste1[i])

        # vérifier le fonctionnement bouton back
        self.browser.find_element('tag name', 'a').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        self.assertIn('number of contacts:', self.browser.find_element('id', 'count_contacts').text)
        time.sleep(1)

        # fermeture de l'application à la fin des tests
        self.browser.close()
        
        
        