# Je lance les tests fonctionnels avec ce fichier
import os

# TITRE RNCP
os.system("python manage.py test functional_tests.tests_addContact_form --keepdb")

# GLOBAUX
#os.system("python manage.py test functional_tests.tests_connection_app --keepdb")
#os.system("python manage.py test functional_tests.tests_contacts_pages --keepdb")
#os.system("python manage.py test functional_tests.tests_contact_forms --keepdb")

# CONNECTION_APP
#os.system("python manage.py test functional_tests.connection_app.tests_connection_page --keepdb")
#os.system("python manage.py test functional_tests.connection_app.tests_signup_page --keepdb")
#os.system("python manage.py test functional_tests.connection_app.tests_logout --keepdb")

# CONTACTS_PAGES
#os.system("python manage.py test functional_tests.contacts_pages.tests_check_navigation --keepdb")
#os.system("python manage.py test functional_tests.contacts_pages.tests_contacts_page --keepdb")
#os.system("python manage.py test functional_tests.contacts_pages.tests_networks_page --keepdb")
#os.system("python manage.py test functional_tests.contacts_pages.tests_parties_page --keepdb")
#os.system("python manage.py test functional_tests.contacts_pages.tests_calendar_page --keepdb")

# CONTACT_FORMS
#os.system("python manage.py test functional_tests.contact_forms.tests_addContact_form --keepdb")
#os.system("python manage.py test functional_tests.contact_forms.tests_contactDetails_form --keepdb")
#os.system("python manage.py test functional_tests.contact_forms.tests_editContact_form --keepdb")
#os.system("python manage.py test functional_tests.contact_forms.tests_deleteContact_form --keepdb")