from django.utils.timezone import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.db import models
from django.conf import settings
import itertools
from ourcalendar.logic.intervals import Interval
from user_accounts.models import UserProfile

# TODO Look at this in future for possible inheritance implementation http://blog.headspin.com/?p=474


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

    def get_between(self, range_start, range_end):
        return list(itertools.chain([e.get_between(range_start, range_end) for e in self.events.all()]))

# TODO here to refactor to signals.py
@receiver(post_save, sender=UserProfile)
def create_calendar(sender, instance, created, **kwargs):
    if created:
        Calendar.objects.create(owner=instance, title='Default', color='#267F00')


def hour_from_now():
    return timezone.now() + timezone.timedelta(hours=1)


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, related_name='events')
    title = models.CharField(max_length=200, default='New Event')
    # TODO: validate start < end
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=hour_from_now)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=600, blank=True)

    DEFAULT_TIME_FMT = '%Y-%m-%dT%H:%M:%S'

    def __unicode__(self):
        return "%s -> %s : %s -> %s" % (self.calendar, self.title, self.start, self.end)

    # Serializes the event for the fullcalendar
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start.strftime(getattr(settings, 'TIME_FMT',
                                                 self.DEFAULT_TIME_FMT)),
            'end': self.end.strftime(getattr(settings, 'TIME_FMT',
                                             self.DEFAULT_TIME_FMT)),
            'location': self.location,
            'description': self.description,
        }

    # Returns an Interval for comparison operations
    @property
    def as_interval(self):
        return Interval(self.start, self.end)

    # Returns whether or not a datetime is in the range of the event
    def happens_when(self, time):
        return self.start < time < self.end

    # Gets events between the range_start and range_end. Need these checks to get proper subclass
    def get_between(self, range_start, range_end):
        subclass = self.recurrence_type

        if self.recurrence_type.__class__.__name__.lower() == 'recurrencetype':
            try:
                subclass = self.recurrence_type.singlerecurrence
            except SingleRecurrence.DoesNotExist:
                try:
                    subclass = self.recurrence_type.weeklyrecurrence
                except WeeklyRecurrence.DoesNotExist:
                    pass

        range_start = range_start if range_start is not None else datetime.strptime('1990-01-01 12:12', '%Y-%m-%d %H:%M')
        range_end = range_end if range_end is not None else datetime.strptime('2050-01-01 12:12', '%Y-%m-%d %H:%M')

        return subclass.get_between(range_start, range_end)


class RecurrenceType(models.Model):

    event = models.OneToOneField(Event, primary_key=True, related_name="recurrence_type")

    def get_between(self, range_start, range_end):
        raise NotImplementedError("Recurrence Type not implemented!!")

    @property
    def type(self):
        pass

    def __unicode__(self):
        return "%s -> RecurrenceType" % self.event


class SingleRecurrence(RecurrenceType):

    # If it's just a single event, we just have to make one check

    def get_between(self, range_start, range_end):

        if self.event.start <= range_end and self.event.end >= range_start:
            return self.event
        else:
            return []

    @property
    def type(self):
        return "single"

    def __unicode__(self):
        return "%s -> SingleRecurrenceType" % self.event


class WeeklyRecurrence(RecurrenceType):
    # TODO: Make sure that the length is only 7!
    # TODO: Make sure at least one day is 1
    # TODO: CAUTION: event.start is not necessarily the first date in the recurring series
    # Days of the week, M T W TH F Sa Su
    days_of_week = models.CharField(default="1000000", max_length=7)
    # The number of weeks between each occurrence
    frequency = models.IntegerField(default=1)

    last_event_end = models.DateTimeField(default=hour_from_now)

    # TODO: implement with frequency
    def get_between(self, range_start, range_end):

        # An array of events to return
        events = []
        if self.event.start <= range_end and self.last_event_end >= range_start:
            # Can't be max (self.event.start, range_start) because frequency needs to be calc. from start
            start = self.event.start
            end = min(self.last_event_end, range_end)
            while start <= end:

                if self.days_of_week[start.weekday()] == '1' and start >= range_start:
                    event = Event(calendar=self.event.calendar,
                                  title=self.event.title,
                                  location=self.event.location,
                                  description=self.event.description,
                                  start=start,
                                  end=start + (self.event.end - self.event.start),
                                  id=self.event.id)
                    events.append(event)
                    event.recurrence_type = WeeklyRecurrence()
                if start.weekday() == 6:
                    start = start + timezone.timedelta(days=1) + timezone.timedelta(weeks=self.frequency - 1)
                else:
                    start = start + timezone.timedelta(days=1)

        return events

    @property
    def type(self):
        return "weekly"

    def __unicode__(self):
        return "%s -> WeeklyRecurrenceType" % self.event