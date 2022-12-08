#for calendar
from __future__ import unicode_literals

from datetime import date
from django.db import models
from connection_app.models import User

#for calendar
from django.core.exceptions import ValidationError
from django.urls import reverse


class Contact(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, verbose_name='E-mail', blank=True)
    telephone1 = models.CharField(max_length=30, verbose_name='telephone n°1', blank=True)
    telephone2 = models.CharField(max_length=30, verbose_name='telephone n°2', blank=True)
    profile_photo = models.ImageField(verbose_name='picture', upload_to='image/', default='image/no-image.png')
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return f'{self.id} : {self.first_name} {self.last_name} ({self.fk_user.username})'


class Network(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    network_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['first_name','last_name', 'network_name']

    def __str__(self):
        return f'{self.id} : {self.first_name} {self.last_name} {self.network_name} ({self.fk_user.username})'


class Party(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    party_name = models.CharField(max_length=30, verbose_name='Kind')
    party_date = models.CharField(max_length=30, verbose_name='Date')
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['first_name','last_name', 'party_name', 'date']

    def __str__(self):
        return f'{self.id} : {self.first_name} {self.last_name} {self.party_name} {self.party_date} ({self.fk_user.username})'