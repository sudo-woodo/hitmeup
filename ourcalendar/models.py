from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.db import models
from user_accounts.models import UserProfile


class Calendar(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='calendars')
    title = models.CharField(max_length=200)
    color_regex = RegexValidator(
        regex=r'^#[\dA-F]{6}',
        message="Color must be in 6-digit hex format."
    )
    color = models.CharField(max_length=7, validators=[color_regex])
    privacy = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s -> %s" % (self.owner, self.title)


@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Calendar.objects.create(owner=instance, title='Default', color='#267F00')


def hour_from_now():
    return timezone.now() + timezone.timedelta(hours=1)


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, related_name='events')
    title = models.CharField(max_length=200, default='New Event')
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=hour_from_now)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=600, blank=True)

    def __unicode__(self):
        return "%s -> %s -> %s" % (self.calendar.owner, self.calendar, self.title)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': self.end.strftime('%Y-%m-%dT%H:%M:%S'),
            'location': self.location,
            'description': self.description,
        }
