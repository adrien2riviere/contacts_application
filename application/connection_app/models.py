from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)

    profile_photo = models.ImageField(verbose_name='Photo de profil', upload_to='image/', blank=True)

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle', default='Abonné')

    REQUIRED_FIELDS = ['first_name','last_name']