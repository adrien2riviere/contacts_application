
import datetime
from django.test import Client, TestCase
from contacts_app import forms
from contacts_app.models import Contact, Network, Party, Event
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

# Create your tests here.

# tester le modèle Contact avec les formulaires et views associés
class TestContactCase(TestCase):

    # créer un objet Contact pour les tests
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )
        self.contact1 = Contact.objects.create( 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            telephone1 = '06 00 00 00 00',
            telephone2 = '04 00 00 00 00',
            fk_user = self.user1
        )
        self.image = 'image/no-image.png'

        # se connecter en tant qu'utilisateur
        self.client = Client()
        self.client.force_login(self.user1)

        # mettre en place les urls
        self.contacts_url = reverse('contacts')
        self.add_contact_url = reverse('addContact')
        self.contact_details_url = reverse('contactDetails', kwargs={'id' : self.contact1.id,})
        self.edit_contact_url = reverse('editContact', kwargs={'id' : self.contact1.id,})
        self.delete_contact_url = reverse('deleteContact', kwargs={'id' : self.contact1.id,})
    
    # 1 -- verifier que les nouveaux contacts ont l'image par défaut
    def test_contacts(self):
        self.assertEqual(self.contact1.first_name, 'first_name1')
        self.assertEqual(self.contact1.profile_photo, self.image)

    # 2 -- verifier que les champs requis pour le modèle sont les bons
    def test_contacts_required_fields(self):
        def check_required(f):
            if(str(type(f))[32:-2] in ['CharField','EmailField']):
                return not getattr(f, 'blank', False)
            else:
                return not getattr(f, 'null', False)
        #required_fields =[str(type(f))[32:-2] + ' ' + str(f)[21:] for f in Contact._meta.get_fields() if (not getattr(f, 'blank', False) is True)]
        required_fields = [str(type(f))[32:-2] + ' ' + str(f)[21:] for f in Contact._meta.get_fields() if (check_required(f) is True)]
        required_fields = required_fields[1:-2] 
        self.assertEqual(required_fields, ['CharField first_name', 'CharField last_name'])

    # 3 -- verifier le formulaire addContactForm possède les bons champs
    def test_add_contact_form(self):
        form = forms.addContactForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['first_name', 'last_name', 'email', 'telephone1', 'telephone2', 'profile_photo'])
    
    # 4 -- verifier que le formulaire addContactForm fonctionne pour des données valides
    def test_add_contact_form_valid_data(self):
        form = forms.addContactForm(data={
            'first_name' :  'first_name1',
            'last_name' : 'last_name1',
            'email' : 'email1@example.com',
            'telephone1' : '06 00 00 00 01',
            'telephone2' : '02 00 00 00 01',
            'profile_photo' : 'image/no-image.png'
        })
        self.assertTrue(form.is_valid())
    
    # 5 -- verifier que le formulaire addContactForm renvoie une erreur pour chaque entrées invalides
    def test_add_contact_form_no_data(self):
            form = forms.addContactForm(data={
                'first_name' : None,
                'last_name' : None,
                'email' : 'email@example'
                #'profile_photo' form field don't register invalide entry
            })
            self.assertEqual(len(form.errors), 3)
    
    # 6 -- verifier le formulaire editContactForm possède les bons champs
    def test_edit_contact_form(self):
        form = forms.editContactForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['first_name', 'last_name', 'email', 'telephone1', 'telephone2', 'profile_photo'])
    
    # 7 -- verifier que le formulaire editContactForm fonctionne pour des données valides
    def test_edit_contact_form_valid_data(self):
        form = forms.editContactForm(data={
            'first_name' :  'first_name1',
            'last_name' : 'last_name1',
            'email' : 'email1@example.com',
            'telephone1' : '06 00 00 00 01',
            'telephone2' : '02 00 00 00 01',
            'profile_photo' : 'image/no-image.png'
        })
        self.assertTrue(form.is_valid())
    
    # 8 -- verifier que le formulaire editContactForm renvoie une erreur pour chaque entrées invalides
    def test_edit_contact_form_no_valid_data(self):
        form = forms.editContactForm(data={
            'first_name' : None,
            'last_name' : None,
            'email' : 'email@example'
            #'profile_photo' form field don't register invalide entry
        })
        self.assertEqual(len(form.errors), 3)
    
    # 9 -- verifier que l'url "contacts" retourne le bon template sans page d'erreur 
    def test_contacts_template(self):
        response = self.client.get(self.contacts_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts_app/contacts.html')
    
    # 10 -- verifier que l'url "Addcontact" retourne le bon template sans page d'erreur 
    def test_addContact_template(self):
        response = self.client.get(self.add_contact_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactsForms/addContact.html')
    
    # 11 -- verifier que l'url "contactDetails" retourne le bon template sans page d'erreur 
    def test_contact_details_template(self):
        response = self.client.get(self.contact_details_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactsForms/contactDetails.html')
    
    # 12 -- verifier que l'url "editContact" retourne le bon template sans page d'erreur 
    def test_edit_contact_template(self):
        response = self.client.get(self.edit_contact_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactsForms/editContact.html')
    
    # 13 -- verifier que l'url "deleteContact" retourne le bon template sans page d'erreur 
    def test_delete_contact_template(self):
        response = self.client.get(self.delete_contact_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactsForms/deleteContact.html')
    

# tester le modèle Network avec les formulaires et views associés
class TestNetworkCase(TestCase):

    # créer un objet Network pour les tests
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )
        self.network1 = Network.objects.create( 
            first_name="first_name1", 
            last_name ='last_name1', 
            network_name = 'network1', 
            user_name = 'user_name1',
            fk_user = self.user1
        )

        # se connecter en tant qu'utilisateur
        self.client = Client()
        self.client.force_login(self.user1)

        # mettre en place les urls
        self.networks_url = reverse('networks')
        self.add_network_url = reverse('addNetwork')
        self.network_details_url = reverse('networkDetails', kwargs={'id' : self.network1.id,})
        self.edit_network_url = reverse('editNetwork', kwargs={'id' : self.network1.id,})
        self.delete_network_url = reverse('deleteNetwork', kwargs={'id' : self.network1.id,})
    
    # 14 -- verifier que la création d'un nouveau network fonctionne
    def test_networks(self):
        self.assertEqual(self.network1.first_name, 'first_name1')

    # 15 -- verifier que les champs requis pour le modèle sont les bons
    def test_networks_required_fields(self):
        def check_required(f):
            if(str(type(f))[32:-2] in ['CharField','EmailField']):
                return not getattr(f, 'blank', False)
            else:
                return not getattr(f, 'null', False)
        #required_fields =[str(type(f))[32:-2] + ' ' + str(f)[21:] for f in Contact._meta.get_fields() if (not getattr(f, 'blank', False) is True)]
        required_fields = [str(type(f))[32:-2] + ' ' + str(f)[21:] for f in Network._meta.get_fields() if (check_required(f) is True)]
        required_fields = required_fields[1:-1] 
        self.assertEqual(required_fields, ['CharField first_name', 'CharField last_name','CharField network_name','CharField user_name'])

    # 16 -- verifier le formulaire addNetworkForm possède les bons champs
    def test_add_network_form(self):
        form = forms.addNetworkForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['first_name', 'last_name','network_name','user_name'])
    
    # 17 -- verifier que le formulaire addNetworkForm fonctionne pour des données valides
    def test_add_network_form_valid_data(self):
        form = forms.addNetworkForm(data={
            'first_name' :  'first_name1',
            'last_name' : 'last_name1',
            'network_name' : 'network_name1',
            'user_name' : 'user_name1',
        })
        self.assertTrue(form.is_valid())
    
    # 18 -- verifier que le formulaire addNetworkForm renvoie une erreur pour chaque entrées invalides
    def test_add_network_form_no_data(self):
            form = forms.addNetworkForm(data={
                'first_name' : None,
                'last_name' : None,
                'network_name' : None,
                'user_name' : None
            })
            self.assertEqual(len(form.errors), 4)
    
    # 19 -- verifier le formulaire editNetworkForm possède les bons champs
    def test_edit_network_form(self):
        form = forms.editNetworkForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['first_name', 'last_name', 'network_name', 'user_name'])
    
    # 20 -- verifier que le formulaire editNetworkForm fonctionne pour des données valides
    def test_edit_network_form_valid_data(self):
        form = forms.editNetworkForm(data={
            'first_name' :  'first_name1',
            'last_name' : 'last_name1',
            'network_name' : 'network_name1',
            'user_name' : 'user_name1'
        })
        self.assertTrue(form.is_valid())

    # 21 -- verifier que le formulaire editNetworkForm renvoie une erreur pour chaque entrées invalides
    def test_edit_network_form_no_data(self):
        form = forms.editNetworkForm(data={
            'first_name' :  None,
            'last_name' : None,
            'network_name' : None,
            'user_name' : None,
        })
        self.assertEqual(len(form.errors), 4)
    
    # 22 -- verifier que l'url "networks" retourne le bon template sans page d'erreur 
    def test_networks_template(self):
        response = self.client.get(self.networks_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts_app/networks.html')
    
    # 23 -- verifier que l'url "AddNetwork" retourne le bon template sans page d'erreur 
    def test_add_network_template(self):
        response = self.client.get(self.add_network_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'networksForms/addNetwork.html')
    
    # 24 -- verifier que l'url "networkDetails" retourne le bon template sans page d'erreur 
    def test_network_details_template(self):
        response = self.client.get(self.network_details_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'networksForms/networkDetails.html')
    
    # 25 -- verifier que l'url "editNetwork" retourne le bon template sans page d'erreur 
    def test_edit_network_template(self):
        response = self.client.get(self.edit_network_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'networksForms/editNetwork.html')
    
    # 26 -- verifier que l'url "deleteNetwork" retourne le bon template sans page d'erreur 
    def test_delete_network_template(self):
        response = self.client.get(self.delete_network_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'networksForms/deleteNetwork.html')


# tester le modèle Party avec les formulaires et views associés
class TestPartyCase(TestCase):

    # créer un objet Party pour les tests
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )
        self.party1 = Party.objects.create( 
            first_name="first_name1", 
            last_name ='last_name1', 
            party_name = 'party_name1',
            party_date = '01 January',
            fk_user = self.user1
        )

        # se connecter en tant qu'utilisateur
        self.client = Client()
        self.client.force_login(self.user1)

        # mettre en place les urls
        self.parties_url = reverse('parties')
        self.add_party_url = reverse('addParty')
        self.party_details_url = reverse('partyDetails', kwargs={'id' : self.party1.id,})
        self.edit_party_url = reverse('editParty', kwargs={'id' : self.party1.id,})
        self.delete_party_url = reverse('deleteParty', kwargs={'id' : self.party1.id,})
    
    # 27 -- verifier que la création d'un nouveau party fonctionne
    def test_parties(self):
        self.assertEqual(self.party1.first_name, 'first_name1')

    # 28 -- verifier que les champs requis pour le modèle sont les bons
    def test_parties_required_fields(self):
        def check_required(f):
            if(str(type(f))[32:-2] in ['CharField','EmailField']):
                return not getattr(f, 'blank', False)
            else:
                return not getattr(f, 'null', False)
        #required_fields =[str(type(f))[32:-2] + ' ' + str(f)[21:] for f in Contact._meta.get_fields() if (not getattr(f, 'blank', False) is True)]
        required_fields = [str(type(f))[32:-2] + ' ' + str(f)[19:] for f in Party._meta.get_fields() if (check_required(f) is True)]
        required_fields = required_fields[1:-1] 
        self.assertEqual(required_fields, ['CharField first_name', 'CharField last_name','CharField party_name','CharField party_date'])

    # 29 -- verifier le formulaire addPartyForm possède les bons champs
    def test_add_party_form(self):
        form = forms.addPartyForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['first_name', 'last_name','party_name','party_date'])
    
    # 30 -- verifier que le formulaire addPartyForm fonctionne pour des données valides
    def test_add_party_form_valid_data(self):
        form = forms.addPartyForm(data={
            'first_name' :  'first_name1',
            'last_name' : 'last_name1',
            'party_name' : 'party_name1',
            'party_date' : '01 January',
        })
        self.assertTrue(form.is_valid())
    
    # 31 -- verifier que le formulaire addPartyForm renvoie une erreur pour chaque entrées invalides
    def test_add_party_form_no_data(self):
            form = forms.addPartyForm(data={
                'first_name' : None,
                'last_name' : None,
                'party_name' : None,
                'party_date' : None
            })
            self.assertEqual(len(form.errors), 4)
    
    # 32 -- verifier le formulaire editPartyForm possède les bons champs
    def test_edit_party_form(self):
        form = forms.editPartyForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['first_name', 'last_name', 'party_name', 'party_date'])
    
    # 33 -- verifier que le formulaire editPartyForm fonctionne pour des données valides
    def test_edit_party_form_valid_data(self):
        form = forms.editPartyForm(data={
            'first_name' :  'first_name1',
            'last_name' : 'last_name1',
            'party_name' : 'party_name1',
            'party_date' : '01 January'
        })
        self.assertTrue(form.is_valid())

    # 34 -- verifier que le formulaire editPartyForm renvoie une erreur pour chaque entrées invalides
    def test_edit_party_form_no_data(self):
        form = forms.editPartyForm(data={
            'first_name' :  None,
            'last_name' : None,
            'party_name' : None,
            'party_date' : None,
        })
        self.assertEqual(len(form.errors), 4)
    
    # 35 -- verifier que l'url "parties" retourne le bon template sans page d'erreur 
    def test_parties_template(self):
        response = self.client.get(self.parties_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts_app/parties.html')
    
    # 36 -- verifier que l'url "AddParty" retourne le bon template sans page d'erreur 
    def test_add_party_template(self):
        response = self.client.get(self.add_party_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'partiesForms/addParty.html')
    
    # 37 -- verifier que l'url "partyDetails" retourne le bon template sans page d'erreur 
    def test_party_details_template(self):
        response = self.client.get(self.party_details_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'partiesForms/partyDetails.html')
    
    # 38 -- verifier que l'url "editParty" retourne le bon template sans page d'erreur 
    def test_edit_party_template(self):
        response = self.client.get(self.edit_party_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'partiesForms/editParty.html')
        
    # 39 -- verifier que l'url "deleteParty" retourne le bon template sans page d'erreur 
    def test_delete_party_template(self):
        response = self.client.get(self.delete_party_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'partiesForms/deleteParty.html')


# tester le modèle Event avec les formulaires et views associés
class TestEventCase(TestCase):

    # créer un objet Event pour les tests
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name1', 
            email = 'email1@example.com', 
            password = 'password1'
        )
        self.event1 = Event.objects.create( 
            Text="Task1 10h", 
            Date = datetime.date(2023, 4, 10), 
            fk_user = self.user1
        )

        # se connecter en tant qu'utilisateur
        self.client = Client()
        self.client.force_login(self.user1)

        # mettre en place les urls
        self.calendar_url = reverse('calendar', kwargs={'page' : 0,})
        self.calendar_url_next_month = reverse('calendar', kwargs={'page' : 1,})
        self.add_event_url = reverse('addEvent', kwargs={'date' : datetime.date(2023, 4, 10), 'page': 1})
        self.manage_event_url = reverse('manageEvent', kwargs={'id' : self.event1.id, 'page': 1})
        self.delete_event_url = reverse('deleteEvent', kwargs={'id' : self.event1.id, 'page': 1})
    
    # 40 -- verifier que la création d'un nouveau event fonctionne
    def test_events(self):
        self.assertEqual(self.event1.Text, 'Task1 10h')

    # 41 -- verifier que les champs requis pour le modèle sont les bons
    def test_event_required_fields(self):
        def check_required(f):
            if(str(type(f))[32:-2] in ['TextField']):
                return not getattr(f, 'blank', False)
            else:
                return not getattr(f, 'null', False)
        #required_fields =[str(type(f))[32:-2] + ' ' + str(f)[21:] for f in Contact._meta.get_fields() if (not getattr(f, 'blank', False) is True)]
        required_fields = [str(type(f))[32:-2] + ' ' + str(f)[19:] for f in Event._meta.get_fields() if (check_required(f) is True)]
        required_fields = required_fields[1:-1] 
        self.assertEqual(required_fields, ['TextField Text', 'DateField Date'])

    # 42 -- verifier le formulaire eventForm possède les bons champs
    def test_event_form(self):
        form = forms.eventForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['Text'])
    
    # 43 -- verifier que le formulaire eventForm fonctionne pour des données valides
    def test_event_form_valid_data(self):
        form = forms.eventForm(data={
            'Text' :  'Task1 10h',
            'Date' : datetime.date(2023, 4, 10)
        })
        self.assertTrue(form.is_valid())
    
    # 44 -- verifier que le formulaire eventForm renvoie une erreur pour chaque entrée invalide
    def test_event_form_no_data(self):
            form = forms.eventForm(data={
                'Text' :  ''
            })
            self.assertEqual(len(form.errors), 1)
    
    # 45 -- verifier que l'url "calendar" retourne le bon template sans page d'erreur 
    def test_calendar_template(self):
        response1 = self.client.get(self.calendar_url)
        response2 = self.client.get(self.calendar_url_next_month)
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response1, 'contacts_app/calendar.html')
        self.assertTemplateUsed(response2, 'contacts_app/calendar.html')
    
    # 46 -- verifier que l'url "AddEvent" retourne le bon template sans page d'erreur 
    def test_add_event_template(self):
        response = self.client.get(self.add_event_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendarForms/addEvent.html')

    # 47 -- verifier que l'url "manageEvent" retourne le bon template sans page d'erreur 
    def test_manage_event_template(self):
        response = self.client.get(self.manage_event_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendarForms/manageEvent.html')
    
    # 48 -- verifier que l'url "deleteEvent" retourne le bon template sans page d'erreur 
    def test_delete_event_template(self):
        response = self.client.get(self.delete_event_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendarForms/deleteEvent.html')