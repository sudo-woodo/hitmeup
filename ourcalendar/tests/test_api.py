import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils.crypto import get_random_string
from ourcalendar.models import Calendar, Event
from util.factories import EventFactory, UserFactory, SingleRecurrenceFactory


class EventApiTestCase(TestCase):
    NUM_EVENTS = 5
    LIST_URL = reverse('events_api:api_event_list')
    GET_DETAIL_URL = lambda self, pk: reverse(
        'events_api:api_event_detail', args=[pk])

    def setUp(self):
        # Create a user (and his/her calendar)
        password = get_random_string()
        user = UserFactory(password=password)
        self.profile = user.profile
        self.calendar = Calendar.objects.get(owner=self.profile)

        # Add some events to the user's calendar
        self.events = [
            EventFactory(calendar=self.calendar) for _ in range(self.NUM_EVENTS)
        ]

        # Turn all those events into single events
        for event in self.events:
            SingleRecurrenceFactory(event=event)

        # Set up client
        self.client = Client()
        self.client.login(username=user.username,
                          password=password)

        # Valid data for testing event update and create
        self.NEW_DATA = {
            'start': '2015-12-12 08:00',
            'end': '2015-12-12 11:00',
            'title': 'Birthday Bash',
            'description': 'A swell time',
            'location': 'Everywhere',
            'last_event':  '2016-1-12 08:00',
            'days_of_week': '1000000',
            'frequency': '1',
            'recurrence_type': 'single'
        }
        self.LIST_DATA= {
            'range_start': '2015-12-12 08:00',
            'range_end': '2015-12-12 11:00'
        }

    def test_auth(self):
        # Tests if request rejected when not authenticated
        anon_client = Client()
        response = anon_client.get(self.LIST_URL)
        self.assertEqual(response.status_code, 401)
        response = anon_client.get(self.GET_DETAIL_URL(EventFactory().pk))
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Tests if list api works
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']

        # Check if we see all the events
        self.assertEqual(len(data), self.NUM_EVENTS)

        # Check if all the events are there
        event_ids = [e.id for e in Event.objects.filter(calendar__owner=self.profile)]
        for user in data:
            self.assertIn(user['event_id'], event_ids)

    def test_detail(self):
        event = self.events[0]

        # Tests if we can get info on a given event
        response = self.client.get(self.GET_DETAIL_URL(event.pk))
        data = json.loads(response.content)

        expected_fields = ['event_id', 'start', 'end', 'title',
                           'calendar', 'location', 'description']

        # Ensure all the fields are present
        for field in expected_fields:
            if field == 'event_id':
                self.assertEqual(data[field], event.pk)
            elif field == 'calendar':
                self.assertEqual(data[field], event.calendar.pk)
            elif field == 'start' or field == 'end':
                # Response contains a 'T' separating date and time
                self.assertEqual(data[field].replace('T', ' '),
                                 str(getattr(event, field)))
            else:
                self.assertEqual(data[field], getattr(event, field))

    def test_update(self):
        # Create a event that belongs to another user
        new_event = EventFactory()

        # Try to update an event that isn't ours
        response = self.client.put(self.GET_DETAIL_URL(new_event.pk),
                                   json.dumps({'title': 'New title'}))

        # Ensure we are unauthorized to do so, and field is unchanged
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(Event.objects.get(pk=new_event.pk), 'New title')

        # Arbitrary event that we will modify in this test
        event = self.events[0]

        # Try update with invalid start date
        response = self.client.put(self.GET_DETAIL_URL(event.pk),
                                   json.dumps({'start': 'not/a/date'}))
        data = json.loads(response.content)

        # Test error occurs and field not changed
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertNotEqual(Event.objects.get(pk=event.pk).start, 'not/a/date')

        # Try update with invalid end date
        response = self.client.put(self.GET_DETAIL_URL(event.pk),
                                   json.dumps({'end': 'not/a/date'}))
        data = json.loads(response.content)

        # Test error occurs and field not changed
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertNotEqual(Event.objects.get(pk=event.pk).end, 'not/a/date')

        # Test some valid data with invalid date
        response = self.client.put(self.GET_DETAIL_URL(event.pk),
                                   json.dumps({'end': 'not/a/date',
                                               'title': 'A good title'}))
        data = json.loads(response.content)

        # Test error occurs and field not changed
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertNotEqual(Event.objects.get(pk=event.pk).end, 'not/a/date')
        self.assertNotEqual(Event.objects.get(pk=event.pk).title, 'A good title')

        # Try updating event with the valid data
        response = self.client.put(self.GET_DETAIL_URL(event.pk),
                                   json.dumps(self.NEW_DATA))
        data = json.loads(response.content)

        # Ensure all the fields are present and updated
        for field in self.NEW_DATA:
            if field == 'start' or field == 'end':
                self.assertEqual(
                    getattr(Event.objects.get(pk=event.pk),
                            field).strftime('%Y-%m-%d %H:%M'),
                    self.NEW_DATA[field])
            else:
                self.assertEqual(data[field], self.NEW_DATA[field])
                self.assertEqual(
                    getattr(Event.objects.get(pk=event.pk), field),
                    self.NEW_DATA[field])

    def test_create(self):
        self.NEW_DATA['calendar'] = 'Default'
        bad_data = [
            # Missing title
            {
                'start': self.NEW_DATA['start'],
                'end': self.NEW_DATA['end'],
                'calendar': self.NEW_DATA['calendar'],
            },
            # Missing start time
            {
                'end': self.NEW_DATA['end'],
                'title': self.NEW_DATA['title'],
                'calendar': self.NEW_DATA['calendar'],
            },
            # Missing end time
            {
                'start': self.NEW_DATA['start'],
                'title': self.NEW_DATA['title'],
                'calendar': self.NEW_DATA['calendar'],
            },
            # Missing calendar
            {
                'start': self.NEW_DATA['start'],
                'end': self.NEW_DATA['end'],
                'title': self.NEW_DATA['title'],
            },
            # Invalid start time
            {
                'start': 'totally invalid',
                'end': self.NEW_DATA['end'],
                'title': self.NEW_DATA['title'],
                'calendar': self.NEW_DATA['calendar'],
            },
            # Invalid end time
            {
                'start': self.NEW_DATA['start'],
                'end': 'totally invalid',
                'title': self.NEW_DATA['title'],
                'calendar': self.NEW_DATA['calendar'],
            },
        ]

        # Creating an event with invalid data should result in error
        for data in bad_data:
            response = self.client.post(self.LIST_URL,
                                        json.dumps(data),
                                        content_type='text/json')
            data = json.loads(response.content)

            # Ensure error occurs
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)

        # Test creating a valid event
        response = self.client.post(self.LIST_URL,
                                    json.dumps(self.NEW_DATA),
                                    content_type='text/json')
        data = json.loads(response.content)
        event_id = data['event_id']

        # Ensure all the fields are present and updated
        for field in self.NEW_DATA:
            if field == 'calendar':
                self.assertEqual(data[field], self.calendar.pk)
            elif field == 'start' or field == 'end':
                self.assertEqual(
                    getattr(Event.objects.get(pk=event_id),
                            field).strftime('%Y-%m-%d %H:%M'),
                    self.NEW_DATA[field])
            elif field == 'frequency' or field == 'days_of_week' or field == 'last_event':
                pass
            elif field == 'recurrence_type':
                if self.NEW_DATA[field] == 'weekly':
                    pass
                    self.assertEqual(data['last_event'], self.NEW_DATA['last_event'])
                    self.assertEqual(data['days_of_week'], self.NEW_DATA['days_of_week'])
                    self.assertEqual(data['frequency'], self.NEW_DATA['frequency'])
            else:
                self.assertEqual(data[field], self.NEW_DATA[field])
                self.assertEqual(
                    getattr(Event.objects.get(pk=event_id), field),
                    self.NEW_DATA[field])

    def test_delete(self):
        # Choose event to delete
        event = self.events[0]

        # Ensure event exists prior to deletion
        self.assertIsNotNone(Event.objects.get(pk=event.pk))

        # Delete the event via the API
        self.client.delete(self.GET_DETAIL_URL(event.pk))

        # Check if event is actually deleted
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(pk=event.pk)