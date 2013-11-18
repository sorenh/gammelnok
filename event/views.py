from django.core.mail import send_mail
from django.shortcuts import render
from django import forms

from event import models

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    attendees = forms.IntegerField()
    email = forms.EmailField()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            attendee = models.Attendee()
            attendee.name = form.cleaned_data['name']
            attendee.email = form.cleaned_data['email']
            attendee.save()

            send_mail('Ny tilmelding til %s' % (event,), Template)
            
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = SignUpForm() # An unbound form

    return render(request, 'singup.html', {
        'form': form,
    })
