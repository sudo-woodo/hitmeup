import datetime # may need to change to cater to django.utils.timezone
from django.test import TestCase
from django.utils import timezone
from util.factories import UserFactory, EventFactory, CalendarFactory, WeeklyRecurrenceFactory

from util.factories import Event, Calendar, RecurrenceType, SingleRecurrence, WeeklyRecurrence

#TODO: test single recurrence,
#TODO: IMPORTANT test when event does not have recurrence and someone tries to access it

class WeeklyRecurrenceTest(TestCase):
    # NOTE! start, end, and last_event aren't required to have events on them. That is dictated by days_of_week
    def setUp(self):
        self.event = EventFactory()

    def test_starts_before_start_ends_before_start(self):
        self.event.start=datetime.datetime(2014, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2014, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1000000'
        self.w.last_event_end = datetime.datetime(2014, 5, 29, 10, 46, 45, 349955)
       # self.w.total_number = 5
        self.assertEquals(self.event.get_between(timezone.now(), timezone.now() + timezone.timedelta(hours=1)),[])

    def test_starts_before_start_ends_before_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1000000'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 27, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 25, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 29, 10, 46, 45, 349955))),
            1)

    def test_starts_before_start_ends_after_end(self):
        self.event.start=timezone.now() - timezone.timedelta(days=1) - timezone.timedelta(hours=1)
        self.event.end=timezone.now() - timezone.timedelta(days=1)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.frequency = 1
        self.w.days_of_week = '1000000'
        self.w.last_event_end = timezone.now() + timezone.timedelta(weeks=6)

        self.assertEquals(len(self.event.get_between(timezone.now(), timezone.now() + timezone.timedelta(days=7))),
            1)


    def test_starts_after_start_ends_before_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1000000'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 27, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 21, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 29, 10, 46, 45, 349955))),
            1)

    def test_starts_after_start_ends_after_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1000000'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 21, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 29, 10, 46, 45, 349955))),
            1)

    def test_starts_after_end_ends_after_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1000000'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 4, 21, 10, 46, 45, 349955),
                              datetime.datetime(2015, 4, 29, 10, 46, 45, 349955))),
            0)

    # these tests assume that start/end date have actual events on them
    def test_starts_on_range_start(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0000010'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 27, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 23, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 29, 10, 46, 45, 349955))),
            1)

    def test_ends_on_range_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0000100'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 29, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 23, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 29, 10, 46, 45, 349955))),
            1)

    def test_starts_on_range_end(self):
        self.event.start=datetime.datetime(2015, 5, 29, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 30, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0000100'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 6, 29, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 23, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 29, 10, 46, 45, 349955))),
            1)

    def test_ends_on_range_start(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0000100'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 29, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2015, 6, 29, 10, 46, 45, 349955))),
            1)

    def test_range_start_between_first_event_start_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0000010'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 29, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 23, 11, 46, 45, 349955),
                              datetime.datetime(2015, 5, 25, 10, 46, 45, 349955))),
            0)

    def test_on_range_end_between_first_event_start_end(self):
        self.event.start=datetime.datetime(2015, 5, 23, 10, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 5, 24, 10, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0000010'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 5, 29, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2015, 5, 21, 10, 46, 45, 349955),
                              datetime.datetime(2015, 5, 23, 11, 46, 45, 349955))),
            1)

    # Test days of week

    def test_days_of_week1(self):
        self.event.start=datetime.datetime(2015, 1, 1, 1, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 1, 2, 1, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1010101'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 12, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2013, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2016, 6, 29, 10, 46, 45, 349955))),
            52 + 52 + 52 + 52)

    def test_days_of_week2(self):
        self.event.start=datetime.datetime(2015, 1, 1, 1, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 1, 2, 1, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '0101010'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 12, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2013, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2016, 6, 29, 10, 46, 45, 349955))),
            52 + 52 + 53)

    def test_days_of_week3(self):
        self.event.start=datetime.datetime(2015, 1, 1, 1, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 1, 2, 1, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1111111'
        self.w.frequency = 1
        self.w.last_event_end = datetime.datetime(2015, 12, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2013, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2016, 6, 29, 10, 46, 45, 349955))),
            365)

    # Test frequency

    def test_frequency1(self):
        self.event.start=datetime.datetime(2015, 1, 1, 1, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 1, 2, 1, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1010101'
        self.w.frequency = 2
        self.w.last_event_end = datetime.datetime(2015, 12, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2013, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2016, 6, 29, 10, 46, 45, 349955))),
            52 + 52)

    def test_frequency2(self):
        self.event.start=datetime.datetime(2015, 1, 1, 1, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 1, 2, 1, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1010101'
        self.w.frequency = 3
        self.w.last_event_end = datetime.datetime(2015, 12, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2013, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2016, 6, 29, 10, 46, 45, 349955))),
            70 )
    def test_frequency3(self):
        self.event.start=datetime.datetime(2015, 1, 1, 1, 46, 45, 349955)
        self.event.end=datetime.datetime(2015, 1, 2, 1, 46, 45, 349955)

        self.w = WeeklyRecurrenceFactory(event=self.event)
        self.w.days_of_week = '1010101'
        self.w.frequency = 4
        self.w.last_event_end = datetime.datetime(2015, 12, 31, 10, 46, 45, 349955)
        self.assertEquals(len(self.event.get_between(datetime.datetime(2013, 5, 29, 10, 46, 45, 349955),
                              datetime.datetime(2016, 6, 29, 10, 46, 45, 349955))),
            13*4)

