from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):

    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    profile_photo = models.ImageField(verbose_name='Photo de profil', upload_to='image/', blank=True)

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle', default='Abonné')

    last_login = datetime.now()

    REQUIRED_FIELDS = ['first_name','last_name']


    def __str__(self):
        return (f'{self.username} ( last login: {self.last_login.day}/{self.last_login.month}/{self.last_login.year}, '
        +f'months: {self.last_login.month+self.last_login.year*12 -datetime.now().year*12 - datetime.now().month} )')