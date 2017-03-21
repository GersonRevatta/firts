from __future__ import unicode_literals

from django.db import models
from django.utils import timezone 
from django.utils import timezone

# Create your models here.

'''
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label

    def __unicode__(self):
        return self.label
'''
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label

    def __unicode__(self):
        return self.label

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    #timestamp = models.DateTimeField(default=timezone.now(), db_index=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    def __str__(self):
        return self.__unicode__()

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
