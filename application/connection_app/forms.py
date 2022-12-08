from wsgiref.validate import validator
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='User name', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
    username = forms.CharField(max_length=30)
    email = forms.CharField(max_length=40)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)