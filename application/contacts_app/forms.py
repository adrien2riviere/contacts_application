from django import forms
from contacts_app.models import Contact, Network, Party


#class addContactForm(forms.Form):
#    first_name = forms.CharField(max_length=254, label='First name', required=True)
#    last_name = forms.CharField(max_length=254, label='Last name', required=True)
#    email = forms.EmailField(max_length=254)
#    telephone1 = forms.CharField(max_length=20, label='Telephone n°1')
#    telephone2 = forms.CharField(max_length=20, label='Telephone n°2')
#    photo = models.ImageField(verbose_name='Picture', upload_to = "image/", blank=True)


class addContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'telephone1', 'telephone2', 'profile_photo')

class editContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'telephone1', 'telephone2', 'profile_photo')

class deleteContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ()


class addNetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ('first_name', 'last_name', 'network_name', 'user_name')

class editNetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ('first_name', 'last_name', 'network_name', 'user_name')

class deleteNetworkForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ()


class addPartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ('first_name', 'last_name', 'party_name', 'party_date')

class editPartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ('first_name', 'last_name', 'party_name', 'party_date')

class deletePartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ()
