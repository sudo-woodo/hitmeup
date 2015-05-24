from django.test import TestCase
from django.utils import timezone
from util.factories import CalendarFactory, EventFactory


class CalendarTestCase(TestCase):

    def setUp(self):
        self.calendar = CalendarFactory()
        self.profile = self.calendar.owner

    def test_default(self):
        # Ensure default calendar exists when user profile is created
        self.assertIsNotNone(self.calendar)

        # Test the default values of the calendar are correct
        self.assertEqual(self.calendar.owner, self.profile)
        self.assertEqual(self.calendar.privacy, 0)
        self.assertEqual(str(self.calendar),
                         str(self.profile) + ' -> ' + self.calendar.title)

    def test_create(self):
        # Valid data for calendar creation
        data = {
            'owner': self.profile,
            'title': 'Personal',
            'color': '#420BAE',
            'privacy': 420
        }

        # Create the calendar with the given data
        calendar = CalendarFactory(
            owner=data['owner'],
            title=data['title'],
            color=data['color'],
            privacy=data['privacy']
        )

        # Try accessing all the fields, ensure they're correct
        for field in data:
            self.assertEqual(data[field], getattr(calendar, field))


class EventTestCase(TestCase):

    def setUp(self):
        self.calendar = CalendarFactory()
        self.profile = self.calendar.owner

    def test_create(self):
        # Valid data for an event
        data = {
            'calendar': self.calendar,
            'title': "JoJo's Bizarre Adventure",
            'start': timezone.now(),
            'end': timezone.now() + timezone.timedelta(hours=5),
            'location': 'Great Britain',
            'description': "JoJo's Bizarre Adventure tells the story of "
                           "the Joestar family, a family whose various members "
                           "discover they are destined to take down supernatural "
                           "foes using unique powers that they find they possess."
        }

        # Create the event
        event = EventFactory(
            calendar=data['calendar'],
            title=data['title'],
            start=data['start'],
            end=data['end'],
            location=data['location'],
            description=data['description'],
        )

        # Try accessing all the fields, ensure they're correct
        for field in data:
            self.assertEqual(data[field], getattr(event, field))

        # Serialize the event
        serialized_data = event.serialize()

        # Ensure serialized data is correct
        for field in data:
            # Start and end times should be formatted
            if field == 'start':
                self.assertEqual(event.start.strftime('%Y-%m-%dT%H:%M:%S'),
                                 serialized_data[field])
            elif field == 'end':
                self.assertEqual(event.end.strftime('%Y-%m-%dT%H:%M:%S'),
                                 serialized_data[field])
            elif field == 'calendar':
                pass
            else:
                self.assertEqual(getattr(event, field), serialized_data[field])

        # Test unicode representation
        self.assertEqual(
            "%s -> %s -> %s" % (event.calendar.owner, event.calendar, event.title),
            unicode(event)
        )

    def test_interval(self):
        event = EventFactory()
        interval = event.as_interval
        self.assertEqual(event.start, interval.start)
        self.assertEqual(event.end, interval.end)

    def test_happens_when(self):
        now = timezone.now()
        onehr = timezone.timedelta(hours=1)

        # Test in range
        inrange = EventFactory(
            start=now - onehr,
            end=now + onehr,
        )
        self.assertTrue(inrange.happens_when(now))

        # Test before
        before = EventFactory(
            start=now - 2 * onehr,
            end=now - onehr,
        )
        self.assertFalse(before.happens_when(now))

        # Test edge before
        before = EventFactory(
            start=now - onehr,
            end=now,
        )
        self.assertFalse(before.happens_when(now))

        # Test after
        before = EventFactory(
            start=now + onehr,
            end=now + 2 * onehr,
        )
        self.assertFalse(before.happens_when(now))

        # Test edge after
        before = EventFactory(
            start=now,
            end=now + onehr,
        )
        self.assertFalse(before.happens_when(now))
