from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contacts_app.models import Contact, Network, Party, Event

from .forms import addContactForm, editContactForm
from .forms import addNetworkForm, editNetworkForm
from .forms import addPartyForm, editPartyForm
from .forms import eventForm

from django.db.models.functions import Lower

import datetime

# Create your views here.
@login_required
def contacts(request):
    events = Event.objects.filter(fk_user=request.user.id)
    # delete the old events !!
    for e in events:
        date_now = datetime.datetime.now()
        date_from_now = datetime.datetime(date_now.year, date_now.month-1, 1)
        date_from_event = datetime.datetime(e.Date.year, e.Date.month, 1)
        if(date_from_event < date_from_now):
            e.delete()
    contacts = Contact.objects.filter(fk_user=request.user.id).order_by(Lower('first_name'), Lower('last_name'))
    count = contacts.count()
    return render(request, 'contacts_app/contacts.html', context={'contacts' : contacts, 'count': count})

@login_required
def addContact(request):
    form = addContactForm()
    if request.method == "POST":
        form = addContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.fk_user = request.user
            contact.save()
            return redirect('contacts')
    return render(request, 'contactsForms/addContact.html', context={'form' : form})

@login_required
def contactDetails(request, id):
    contact = Contact.objects.get(id=id)
    if request.user.id == contact.fk_user.id :
        return render(request, 'contactsForms/contactDetails.html', context={'contact' : contact})
    else :
        return redirect('contacts')

@login_required
def editContact(request, id):
    contact = Contact.objects.get(id=id)
    form = editContactForm(initial={
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "email": contact.email,
        "telephone1": contact.telephone1,
        "telephone2": contact.telephone2,
        })
    if request.user.id == contact.fk_user.id :
        if request.method == 'POST':
            form = editContactForm(request.POST, request.FILES)
            if form.is_valid():
                profile_photo = contact.profile_photo
                contact = form.save(commit=False)
                contact.fk_user = request.user
                if contact.profile_photo == 'image/no-image.png':
                    contact.profile_photo = profile_photo
                    contact.id = id
                    contact.save()
                else:
                    if(profile_photo == 'image/no-image.png'):
                        contact.id = id
                        contact.save()
                    else:
                        profile_photo.delete(save=False)
                        contact.id = id
                        contact.save()
        return render(request, 'contactsForms/editContact.html', context={'form': form, 'contact': contact})
    else :
        return redirect('contacts')

@login_required
def deleteContact(request, id):
    contact = Contact.objects.get(id=id)
    if request.user.id == contact.fk_user.id :
        if 'deleteThat' in request.POST:
            contact.delete()
        if request.method == 'POST':
            return redirect('contacts')
        return render(request, 'contactsForms/deleteContact.html', context={'contact': contact})
    else :
        return redirect('contacts')


@login_required
def networks(request):
    networks = Network.objects.filter(fk_user=request.user.id).order_by(Lower('first_name'), Lower('last_name'))
    count = networks.count()
    return render(request, 'contacts_app/networks.html', context={'networks' : networks, 'count': count})

@login_required
def addNetwork(request):
    form = addNetworkForm()
    if request.method == "POST":
        form = addNetworkForm(request.POST)
        if form.is_valid():
            network = form.save(commit=False)
            network.fk_user = request.user
            network.save()
            return redirect('networks')
    return render(request, 'networksForms/addNetwork.html', context={'form' : form})

@login_required
def networkDetails(request, id):
    network = Network.objects.get(id=id)
    if request.user.id == network.fk_user.id :
        return render(request, 'networksForms/networkDetails.html', context={'network' : network})
    else :
        return redirect('contacts')

@login_required
def editNetwork(request, id):
    network = Network.objects.get(id=id)
    form = editNetworkForm(initial={
        "first_name": network.first_name,
        "last_name": network.last_name,
        "network_name": network.network_name,
        "user_name": network.user_name
        })
    if request.user.id == network.fk_user.id :
        if request.method == 'POST':
            form = editNetworkForm(request.POST, request.FILES)
            if form.is_valid():
                network = form.save(commit=False)
                network.fk_user = request.user
                network.id = id
                network.save()
        return render(request, 'networksForms/editNetwork.html', context={'form': form, 'network': network})
    else :
        return redirect('contacts')

@login_required
def deleteNetwork(request, id):
    network = Network.objects.get(id=id)
    if request.user.id == network.fk_user.id :
        if 'deleteThat' in request.POST:
            network.delete()
        if request.method == 'POST':
            return redirect('networks')
        return render(request, 'networksForms/deleteNetwork.html', context={'network': network})
    else :
        return redirect('contacts')


@login_required
def parties(request):
    parties = Party.objects.filter(fk_user=request.user.id).order_by(Lower('first_name'), Lower('last_name'))
    count = parties.count()
    return render(request, 'contacts_app/parties.html', context={'parties' : parties, 'count': count})

@login_required
def addParty(request):
    form = addPartyForm()
    if request.method == "POST":
        form = addPartyForm(request.POST)
        if form.is_valid():
            party = form.save(commit=False)
            party.fk_user = request.user
            party.save()
            return redirect('parties')
    return render(request, 'partiesForms/addParty.html', context={'form' : form})

@login_required
def partyDetails(request, id):
    party = Party.objects.get(id=id)
    if request.user.id == party.fk_user.id :
        return render(request, 'partiesForms/partyDetails.html', context={'party' : party})
    else :
        return redirect('contacts')

@login_required
def editParty(request, id):
    party = Party.objects.get(id=id)
    form = editPartyForm(initial={
        "first_name": party.first_name,
        "last_name": party.last_name,
        "party_name": party.party_name,
        "party_date": party.party_date,
        })
    if request.user.id == party.fk_user.id :
        if request.method == 'POST':
            form = editPartyForm(request.POST, request.FILES)
            if form.is_valid():
                party = form.save(commit=False)
                party.fk_user = request.user
                party.id = id
                party.save()
        return render(request, 'partiesForms/editParty.html', context={'form': form, 'party': party})
    else :
        return redirect('contacts')

@login_required
def deleteParty(request, id):
    party = Party.objects.get(id=id)
    if request.user.id == party.fk_user.id :
        if 'deleteThat' in request.POST:
            party.delete()
        if request.method == 'POST':
            return redirect('parties')
        return render(request, 'partiesForms/deleteParty.html', context={'party': party})
    else :
        return redirect('contacts')


@login_required
def calendar(request, page):
    events = Event.objects.filter(fk_user=request.user.id).order_by('Date')
    count = events.count()
    return render(request, 'contacts_app/calendar.html', context={'events' : events, 'count': count, 'page': page})

@login_required
def addEvent(request, date, page):
    form = eventForm()
    if request.method == "POST":
        form = eventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.Date = datetime.datetime(int(date[6:10]), int(date[3:5]), int(date[0:2]))
            event.fk_user = request.user
            event.save()
            return redirect('calendar', page)
    return render(request, 'calendarForms/addEvent.html', context={'form' : form, 'date': date, 'page': page})

@login_required
def manageEvent(request, id, page):
    event = Event.objects.get(id=id)
    form = eventForm(initial={
        "Text": event.Text,
        })
    if request.user.id == event.fk_user.id :
        if request.method == 'POST':
            form = eventForm(request.POST)
            date = event.Date
            if form.is_valid():
                event = form.save(commit=False)
                event.Date = date
                event.fk_user = request.user
                event.id = id
                event.save()
        return render(request, 'calendarForms/manageEvent.html', context={'form': form, 'event': event, 'page': page})
    else :
        return redirect('contacts')

@login_required
def eventDetails(request, id, page):
    event = Event.objects.get(id=id)
    if request.user.id == event.fk_user.id :
        return render(request, 'calendarForms/eventDetails.html', context={'event' : event, 'page': page})
    else :
        return redirect('contacts')

@login_required
def noEvent(request, page):
    return render(request, 'calendarForms/noEvent.html', context={'page': page})

@login_required
def deleteEvent(request, id, page):
    event = Event.objects.get(id=id)
    if request.user.id == event.fk_user.id :
        date = event.Date.strftime("%d/%m/%Y")
        if 'deleteThat' in request.POST:
            event.delete()
            return redirect('calendar', page)
        if 'btn_cancel' in request.POST:
            return redirect('manageEvent', id, page)
        return render(request, 'calendarForms/deleteEvent.html', context={'date': date, 'page' : page})
    else :
        return redirect('contacts')

