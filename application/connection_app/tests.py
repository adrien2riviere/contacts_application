from django.test import Client, TestCase

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from connection_app import forms

# Create your tests here.
# Chacun des tests est numéroté de 1 à 14

# tester le modèle User
class UserModelTestCase(TestCase):

    # créer un objet User pour les tests
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username = 'user1', 
            first_name="first_name1", 
            last_name ='last_name2', 
            email = 'email1@example.com', 
            password = 'password1'
        )

    # 1 -- verifier que les nouveaux utilisateurs n'ont pas les droits administrateurs
    def test_users(self):
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.is_superuser, False)

    # 2 -- verifier que les champs requis pour le modèle sont les bons
    def test_users_required(self):
        def check_required(f):
            if(str(type(f))[32:-2] == 'Charfield'):
                return not getattr(f, 'blank', False)
            else:
                return not getattr(f, 'null', False)
        #required_fields = [str(type(f))[8:-2] + ' ' + str(f) for f in get_user_model()._meta.get_fields() if (not getattr(f, 'null', False) is True)]
        required_fields = [str(type(f))[32:-2] + ' ' + str(f)[20:] for f in get_user_model()._meta.get_fields() if (check_required(f) == True)]
        required_fields = required_fields[1:-2]
        self.assertEqual(required_fields, 
        ['CharField password', 'BooleanField is_superuser', 'CharField username', 'EmailField email', 'BooleanField is_staff',
        'BooleanField is_active', 'DateTimeField date_joined', 'CharField first_name', 'CharField last_name'])


# tester les formulaires associées au modèle User
class UserFormTestCase(TestCase):

    # 3 -- verifier que le formulaire LoginForm possède les bons champs
    def test_login_form_correct_fields(self):
        form = forms.LoginForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['username', 'password'])

    # 4 -- verifier que le formulaire LoginForm fonctionne pour des données valides
    def test_login_form_valid_data(self):
        form = forms.LoginForm(data={
            'username' : 'user1',
            'password' : 'password1'
        })
        self.assertTrue(form.is_valid())

    # 5 -- verifier que le formulaire LoginForm renvoie une erreur quand un champ est vide
    def test_login_form_no_data(self):
            form = forms.LoginForm(data={
            })
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 2)

    # 6 -- verifier que le formulaire SignUpForm possède les bons champs
    def test_signup_form_correct_fields(self):
        form = forms.SignupForm()
        fields = [ f for f in form.fields.keys()]
        self.assertEqual(fields, ['username', 'email', 'first_name', 'last_name', 'password1', 'password2'])
    
    # 7 -- verifier que le formulaire SignUpForm fonctionne pour des données valides
    def test_signup_form_valid_data(self):
        form = forms.SignupForm(data={
            'username' : 'user2',
            'email' : 'email2@example.com',
            'first_name' : 'first_name2',
            'last_name' : 'last_name2',
            'password1' : 'password2',
            'password2' : 'password2'
        })
        self.assertTrue(form.is_valid())
    
    # 8 -- verifier que le formulaire SignUpForm renvoie une erreur quand un champ n'est pas remplis
    def test_signup_form_no_data(self):
            form = forms.SignupForm(data={
            })
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 6)


# tester les views pour le modèle User
class UserTemplatesCase(TestCase):

    # mettre en place les urls
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')

    # 9 -- verifier que l'url "login" retourne le bon template sans page d'erreur 
    def test_login_template(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'connection_app/login_page.html')

    # 10 -- verifier que l'url "signup" retourne le bon template sans page d'erreur 
    def test_signup_template(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'connection_app/signup.html')
        

# tester les views pour réintialiser les mots de passes
class ResetPasswordTemplatesCase(TestCase):

    # mettre en place les urls
    def setUp(self):
        self.client = Client()
        self.reset_password_url = reverse('reset_password')
        self.password_send_url = reverse('password_reset_done')
        self.password_confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': 'MQ', 'token' : 'aa1v2k-8ab2c9597a4f6cc754e3dc5baaf3c77f'})
        self.password_complete_url = reverse('password_reset_complete')

    # 11 -- verifier que l'url "reset_password" retourne le bon template sans page d'erreur 
    def test_reset_form_template(self):
        response = self.client.get(self.reset_password_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')
    
    # 12 -- verifier que l'url "password_reset_done" retourne le bon template sans page d'erreur 
    def test_reset_send_template(self):
        response = self.client.get(self.password_send_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')
    
    # 13 -- verifier que l'url "password_reset_confirm" retourne le bon template sans page d'erreur 
    def test_reset_confirm_template(self):
        response = self.client.get(self.password_confirm_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')
    
    # 14 -- verifier que l'url "password_reset_complete" retourne le bon template sans page d'erreur 
    def test_reset_complete_template(self):
        response = self.client.get(self.password_complete_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')

