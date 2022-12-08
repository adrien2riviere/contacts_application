"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

import connection_app.views
import contacts_app.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', connection_app.views.login_page, name='login'),
    path('logout', connection_app.views.logout_user, name='logout'),
    path('signup', connection_app.views.signup_page, name='signup'),
    path('home', connection_app.views.home, name='home'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('contacts/', contacts_app.views.contacts, name="contacts"),
    path('contacts/add/', contacts_app.views.addContact, name="addContact"),
    path('contacts/details/<int:id>/', contacts_app.views.contactDetails, name="contactDetails"),
    path('contacts/edit/<int:id>/', contacts_app.views.editContact, name="editContact"),
    path('contacts/deleteContact/<int:id>/', contacts_app.views.deleteContact, name="deleteContact"),

    path('networks/', contacts_app.views.networks, name="networks"),
    path('networks/add', contacts_app.views.addNetwork, name="addNetwork"),
    path('networks/details/<int:id>/', contacts_app.views.networkDetails, name="networkDetails"),
    path('networks/edit/<int:id>/', contacts_app.views.editNetwork, name="editNetwork"),
    path('networks/deleteNetwork/<int:id>/', contacts_app.views.deleteNetwork, name="deleteNetwork"),

    path('parties/', contacts_app.views.parties, name="parties"),
    path('parties/add', contacts_app.views.addParty, name="addParty"),
    path('parties/details/<int:id>/', contacts_app.views.partyDetails, name="partyDetails"),
    path('parties/edit/<int:id>/', contacts_app.views.editParty, name="editParty"),
    path('parties/deleteParty/<int:id>/', contacts_app.views.deleteParty, name="deleteParty"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)