from django.core.urlresolvers import reverse
from django.db import models
from uuidfield import UUIDField

class Event(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    date = models.DateField()

    def __unicode__(self):
        return self.name

    def total_attendees(self):
        return sum([x.number_of_people for x in self.attendees.all()])

class Attendee(models.Model):
    uuid = UUIDField(auto=True, unique=True)
    name = models.CharField(max_length=200)
    number_of_people = models.IntegerField()
    email = models.EmailField()
    event = models.ForeignKey(Event, related_name="attendees")

    def edit_link(self, request):
        return request.build_absolute_uri(reverse('signup_edit',
                                                  kwargs={'uuid': self.uuid}))

    def __unicode__(self):
        return self.name

