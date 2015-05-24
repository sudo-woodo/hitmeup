import datetime # may need to change to cater to django.utils.timezone
from django.test import TestCase
from django.utils import timezone
from util.factories import UserFactory, EventFactory, CalendarFactory, WeeklyRecurrenceFactory

from util.factories import Event, Calendar, RecurrenceType, SingleRecurrence, WeeklyRecurrence



class WeeklyRecurrenceTest(TestCase):
    def setUp(self):
        self.event = EventFactory()

    def test_starts_before_start_ends_before_start(self):
        self.event.start=datetime.datetime(2014, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2014, 5, 25, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = [1,0,0,0,0,0,0]
       # self.w.total_number = 5
        self.assertEquals(self.event.get_between(timezone.now(), timezone.now() + timezone.timedelta(hours=1)),[])

    def test_starts_before_start_ends_before_end(self):
        self.event.start=timezone.now() - timezone.timedelta(days=1) - timezone.timedelta(hours=1)
        self.event.end=timezone.now() - timezone.timedelta(days=1)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        #self.w.total_number = 2
        self.w.days_of_week = [1,0,0,0,0,0,0]

        self.assertEquals(len(self.event.get_between(timezone.now(), timezone.now() + timezone.timedelta(days=7))),
            1)
'''
    def test_starts_before_start_ends_after_end(self):
    self.event.start=timezone.now() - timezone.timedelta(days=1) - timezone.timedelta(hours=1)
        self.event.end=timezone.now() - timezone.timedelta(days=1)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.total_number = 2
        self.w.days_of_week = [1,0,0,0,0,0,0]

        self.assertEquals(len(self.event.get_between(timezone.now(), timezone.now() + timezone.timedelta(days=7))),
            1)
'''
'''
    def test_starts_after_start_ends_before_end(self):

    def test_starts_after_start_ends_after_end(self):

    def test_starts_after_end_ends_before_end(self):

    #tests a mixture of days_of_week, total_number, and frequency
    def test_complex

'''




