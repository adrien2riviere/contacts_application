from django.contrib import admin
from contacts_app.models import Contact, Network, Party

# Register your models here.
admin.site.register(Contact)
admin.site.register(Network)
admin.site.register(Party)