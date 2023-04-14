import json
# import os
from django.test import Client
from django.contrib.auth import get_user_model
from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time
from contacts_app.models import Contact
from django.db.models.functions import Lower

# ----> LE UPDATE DE L'IMAGE NE MARCHE PAS, TESTER A LA MAIN !

class Test0Contact(LiveServerTestCase):

    # mettre en place les urls
    def setUp(self):
        #self.browser =  webdriver.Edge('functional_tests/msedgedriver.exe')
        self.browser =  webdriver.Chrome('functional_tests/chromedriver.exe')
        self.contacts_url = reverse('contacts')
        self.edit_contact_url = reverse('editContact', kwargs={'id' : 2})

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

        # créer les chaines de texte pour la page de mise à jour du contact
        self.first_name = 'Aurelie'
        self.last_name = 'LXXXXX'
        self.email = 'axxxxx@live.fr'
        self.telephone1 = '06 00 00 00 01'
        self.telephone2 = '02 00 00 00 01'

        # créer les chaines de texte pour la page de mise à jour du contact
        self.first_name_bis = 'Aurore'
        self.last_name_bis = 'MXXXXX'
        self.email_bis = 'mxxxxx@gmail.com'
        self.telephone1_bis = '07 00 00 00 02'
        self.telephone2_bis = '04 00 00 00 02'

        # utiliser des images pour les tests
        self.src_no_image = '/image/image/no-image.png'
        self.src_image_tests = '/image/image/image_tests.jpg'
        self.src_image_tests_remove = '/image/image_tests.jpg'


    # test de la fonctionnalité de mise à jour d'un contact
    def test_edit_contact_page(self):

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

        # accéder à la page de mise à jour du contact
        td1 = tr1.find_elements('tag name', 'td')[-1]
        button1 = td1.find_elements('tag name', 'button')[1]
        button1.click()
        time.sleep(1)

        # vérifier l'interface de la page editContact
        self.assertEqual(self.browser.find_element('tag name', 'h1').text, 'Contacts Booklet')
        self.assertEqual(self.browser.find_element('tag name', 'h2').text, 'Update the contact')
        text = self.live_server_url + '/image/image/no-image.png'
        self.assertEqual(self.browser.find_element('tag name', 'img').get_attribute('src'), text)
        liste1 = ['First name:', 'Last name:', 'E-mail:', 'Telephone n°1:', 'Telephone n°2:', 'Picture:']
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('tag name', 'label')[i].text, liste1[i])
        liste1 = [self.first_name, self.last_name, self.email, self.telephone1, self.telephone2]
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('tag name', 'input')[i].get_attribute('value'), liste1[i])

        # vérifier le fonctionnement du bouton back
        self.browser.find_element('tag name', 'a').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.contacts_url)
        self.assertIn('number of contacts:', self.browser.find_element('id', 'count_contacts').text)
        time.sleep(1)

        # retour sur la page editContact
        self.browser.get(self.live_server_url + self.edit_contact_url)
        time.sleep(1)

        # vérifier la limitation des champs en nombre de caractères
        length = len(self.browser.find_elements('tag name', 'input'))
        for i in range(length-1):
            self.browser.find_elements('tag name', 'input')[i].clear()
        time.sleep(1)
        text = 'a_entry_with_more_than_thirty_or_forty_characters'
        liste1 = [text[:30], text[:30], text[:40], text[:30], text[:30]]
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[i].send_keys(text)
            self.assertEqual(self.browser.find_elements('tag name', 'input')[i].get_attribute('value'), liste1[i])
        time.sleep(1)
        
        # tester des champs requis vides
        self.browser.get(self.live_server_url + self.edit_contact_url)
        time.sleep(1)
        length = len(self.browser.find_elements('tag name', 'input'))
        for i in range(length-1):
            self.browser.find_elements('tag name', 'input')[i].clear()
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        contact1 = Contact.objects.filter(fk_user=self.user1.id).order_by(Lower('first_name'), Lower('last_name'))[1]
        self.assertEqual(contact1.first_name, self.first_name)
        time.sleep(1)
        self.browser.find_elements('tag name', 'input')[0].send_keys(self.first_name)
        self.browser.find_element('tag name', 'button').click()
        contact1 = Contact.objects.filter(fk_user=self.user1.id).order_by(Lower('first_name'), Lower('last_name'))[1]
        self.assertEqual(contact1.first_name, self.first_name)
        time.sleep(1)

        # tester le formulaire pour un email au format invalide
        self.browser.find_elements('tag name', 'input')[1].send_keys(self.last_name)
        liste1 = ['email', 'email.fr', 'no_valid@email']
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[2].clear()
            self.browser.find_elements('tag name', 'input')[2].send_keys(liste1[i])
            self.browser.find_element('tag name', 'button').click()
            contact1 = Contact.objects.filter(fk_user=self.user1.id).order_by(Lower('first_name'), Lower('last_name'))[1]
            self.assertEqual(contact1.email, self.email)
            if(liste1[i] == 'no_valid@email'):
                ul = self.browser.find_element('class name', 'errorlist')
                text = 'Enter a valid email address.'
                self.assertEqual(ul.find_element('tag name', 'li').text, text)
            time.sleep(1)

        # tester le formulaire pour des données minimales
        self.browser.find_elements('tag name', 'input')[2].clear()
        time.sleep(1)
        length = len(self.browser.find_elements('tag name', 'input'))
        self.browser.find_element('tag name', 'button').click()
        contact1 = Contact.objects.filter(fk_user=self.user1.id).order_by(Lower('first_name'), Lower('last_name'))[1]
        self.assertEqual(contact1.email + contact1.telephone1 + contact1.telephone2, '')
        time.sleep(1)

        # tester le formulaire pour des données complètes
        liste1 = [self.first_name_bis, self.last_name_bis, self.email_bis, self.telephone1_bis, self.telephone2_bis]
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[i].clear()
        time.sleep(1)
        for i in range(len(liste1)):
            self.browser.find_elements('tag name', 'input')[i].send_keys(liste1[i])
        # text = os.getcwd() + '/functional_tests/image_tests.jpg'
        # self.browser.find_elements('tag name', 'input')[5].send_keys(text)
        time.sleep(1)
        self.browser.find_element('tag name', 'button').click()
        time.sleep(1)

        # vérifier la modification dans la table des contacts
        self.browser.get(self.live_server_url + self.contacts_url)
        liste1 = [self.first_name_bis, self.last_name_bis, self.email_bis, self.telephone1_bis]
        tbody = self.browser.find_element('tag name', 'tbody')
        tr1 = tbody.find_elements('tag name', 'tr')[1]
        for i in range(len(liste1)):
            self.assertEqual(tr1.find_elements('tag name', 'td')[i].text, liste1[i])
        time.sleep(1)

        # vérifier les données modifiées dans la page des détails du contact
        td1 = tr1.find_elements('tag name', 'td')[-1]
        button1 = td1.find_elements('tag name', 'button')[0].click()
        time.sleep(1)
        liste1 = [self.first_name_bis, self.last_name_bis, self.email_bis, self.telephone1_bis, self.telephone2_bis]
        for i in range(len(liste1)):
            self.assertEqual(self.browser.find_elements('class name', 'info')[i].text, liste1[i])

        # supprimer l'image
        # os.remove(os.getcwd() + self.src_image_tests_remove)
        
        # fermeture de l'application à la fin des tests
        self.browser.close()