from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.db import models


class Calendar(models.Model):
    pass


class DummyProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    calendar = models.OneToOneField(Calendar, default=Calendar.objects.create(), related_name='owner')

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        DummyProfile.objects.create(user=instance)


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, related_name='events')
    title = models.CharField(max_length=200)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=600)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': self.end.strftime('%Y-%m-%dT%H:%M:%S'),
            'location': self.location,
            'description': self.description,
        }
