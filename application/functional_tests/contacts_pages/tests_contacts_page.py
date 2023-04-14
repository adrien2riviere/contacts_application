import json
from selenium.webdriver.common.keys import Keys
from django.test import Client
from django.contrib.auth import get_user_model
from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
import time
from contacts_app.models import Contact
from django.db.models.functions import Lower
#from seleniumlogin import force_login # c'est nécessaire pour le login par selenium


class Test0ContactPage(LiveServerTestCase):

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

        # créer les chaines de texte pour tester la barre de filtre
        self.first_name = 'Aurelie'
        self.last_name = 'LXXXXX'

    def test_contacts_page(self):

        # chargement des données de contacts
        file = open("./functional_tests/json_datas.json")
        datas = json.load(file)
        self.count_contacts = len(datas["Contacts"])
        
        # créations des contacts de user1
        for i in range(len(datas["Contacts"])):
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

        # Vérifier l'interface 
        self.assertEqual(self.browser.find_element('tag name', 'h1').text, 'Contacts Booklet')
        nav = self.browser.find_element('class name', 'navigation')
        self.assertEqual(nav.find_element('id', 'span_menu').text, 'menu:')
        self.assertEqual(nav.find_element('id', 'contacts').text, 'contacts')
        self.assertEqual(nav.find_element('id', 'networks').text, 'networks')
        self.assertEqual(nav.find_element('id', 'parties').text, 'parties')
        self.assertEqual(nav.find_element('id', 'calendar').text, 'calendar')
        self.assertEqual(nav.find_element('id', 'log').text, 'log out')
        text = 'Search for first names or last names..'
        self.assertEqual(self.browser.find_element('tag name', 'input').get_attribute('placeholder'), text)
        self.assertEqual(self.browser.find_element('id', 'add_btn').text, 'add +')
        text = 'number of contacts: ' + str(self.count_contacts)
        self.assertEqual(self.browser.find_element('id', 'count_contacts').text, text)
        table = self.browser.find_element('tag name', 'table')
        th_list = table.find_elements('tag name', 'th')
        check_title_list = ['First Name', 'Last Name', 'E-mail', 'Telephone n°1', 'Management']
        for i in range(len(check_title_list)):
            if(th_list[i].text != check_title_list[i]):
                self.assertEqual(False, True)
                break
        self.assertEqual(True, True)

        # Vérifier la présence des contacts
        tbody = self.browser.find_element('tag name', 'tbody')
        tr_list = tbody.find_elements('tag name', 'tr')
        tr_list_count = len(tr_list)
        self.assertEqual(tr_list_count, self.count_contacts)

        # Vérifier un contact en particulier
        contact1 = Contact.objects.filter(fk_user=self.user1.id).order_by(Lower('first_name'), Lower('last_name'))[1]
        tr1 = tr_list[1]
        td_list = tr1.find_elements('tag name', 'td')
        check_info_list = [contact1.first_name, contact1.last_name, contact1.email, contact1.telephone1]
        # check_info_list = ['Aurelie', 'LXXXXX', 'axxxxx@live.fr', '06 00 00 00 01']
        for i in range(len(check_info_list)):
            if(td_list[i].text != check_info_list[i]):
                self.assertEqual(False, True)
                break
        self.assertEqual(True, True)
  
        # tester la barre de filtre
        input = self.browser.find_element('tag name', 'input')
        tbody = self.browser.find_element('tag name', 'tbody')
        tr_list = tbody.find_elements('tag name', 'tr')
        liste1 = [self.first_name, self.last_name]
        for i in range(len(liste1)):
            input.send_keys(liste1[i])
            time.sleep(1)
            tr_visible = 0
            tr_expected = 0
            for tr_element in tr_list:
                if(tr_element.get_attribute('style') != "display: none;"):
                    tr_visible +=1
                    tr1 = tr_element
                if(tr_element.find_elements('tag name', 'td')[i].text == liste1[i]):
                    tr_expected += 1
            self.assertEqual(tr_expected, tr_visible)
            self.assertEqual(liste1[i], tr1.find_elements('tag name', 'td')[i].text)
            input.send_keys(Keys.CONTROL, 'a'), input.send_keys(Keys.DELETE) # input.clear() doesn't work well
            time.sleep(1)

        # tester la barre de défilement
        js_script = "document.getElementsByTagName('tbody')[0].scroll(0, document.getElementsByTagName('tbody')[0].scrollHeight)"
        self.browser.execute_script(js_script,"")
        time.sleep(1)
        js_script = "return document.getElementsByTagName('tbody')[0].scrollTop"
        scroll = int(self.browser.execute_script(js_script,""))
        self.assertTrue(scroll > 0)
        time.sleep(1)

        # tester la mise en couleur d'une ligne
        self.browser.get(self.live_server_url + self.contacts_url)
        time.sleep(1)
        tbody = self.browser.find_element('tag name', 'tbody')
        tr1 = tbody.find_elements('tag name', 'tr')[1]
        tr1.click()
        self.assertEqual(tr1.get_attribute("class"), "selected") # vérifier visuellement
        time.sleep(1)
        tr1.click()
        self.assertEqual(tr1.get_attribute("class"), "") # vérifier visuellement
        time.sleep(1)
        
        # fermeture de l'application à la fin des tests
        self.browser.close()