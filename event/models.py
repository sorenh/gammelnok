from django.db import models
from uuidfield import UUIDField

class Event(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

class Attendee(models.Model):
    uuid = UUIDField(auto=True, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    event = models.ForeignKey(Event)
