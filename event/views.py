import datetime
from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from event import models

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    number_of_people = forms.IntegerField(initial=1)
    email = forms.EmailField()

def front(request):
    return HttpResponseRedirect(reverse('signup_top'))

def signup_top(request):
    now = datetime.datetime.now()
    upcoming_events = models.Event.objects.filter(date__gt=now)
    if len(upcoming_events) == 1:
        event = upcoming_events[0]
        return HttpResponseRedirect(reverse('signup',
                                            kwargs={'event_id': event.id}))
    else:
        return render(request, 'upcoming_events.html', {
            'upcoming_events': upcoming_events,
        })


def thanks(request, event_id):
    event = get_object_or_404(models.Event, id=event_id)
    return render(request, 'thanks.html', {
        'event': event,
    })

def signup_edit(request, uuid):
    attendee = get_object_or_404(models.Attendee, uuid=uuid)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            attendee.name = form.cleaned_data['name']
            attendee.number_of_people = form.cleaned_data['number_of_people']
            attendee.email = form.cleaned_data['email']
            attendee.save()

            context = {'event': attendee.event,
                       'attendee': attendee,
                       'request': request,
                       'edit_link': attendee.edit_link(request)}

            return HttpResponseRedirect(reverse('thanks',
                                                kwargs={'event_id': attendee.event.id}))
    else:
        form = SignUpForm({'name': attendee.name,
                           'number_of_people': attendee.number_of_people,
                           'email': attendee.email})

    return render(request, 'signup.html', {
        'form': form,
        'event': attendee.event,
    })    

def signup(request, event_id):
    event = get_object_or_404(models.Event, id=event_id)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            attendee = models.Attendee()
            attendee.name = form.cleaned_data['name']
            attendee.number_of_people = form.cleaned_data['number_of_people']
            attendee.email = form.cleaned_data['email']
            attendee.event = event
            attendee.save()

            context = {'event': event,
                       'attendee': attendee,
                       'request': request,
                       'edit_link': attendee.edit_link(request)}

            # Send confirmation to attendee
            send_mail(render_to_string('mail/attendee/subject.txt', context).strip(),
                      render_to_string('mail/attendee/body.txt', context),
                      event.email,
                      [attendee.email],
                      fail_silently=False)

            # Send notification to coordinator
            send_mail(render_to_string('mail/coordinator/subject.txt', context).strip(),
                      render_to_string('mail/coordinator/body.txt', context),
                      event.email,
                      [event.email],
                      fail_silently=False)
            
            return HttpResponseRedirect(reverse('thanks',
                                                kwargs={'event_id': event.id}))
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {
        'form': form,
        'event': event,
    })
