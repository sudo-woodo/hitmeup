from collections import defaultdict
import itertools
from datetime import timedelta
from restless.dj import DjangoResource
from restless.exceptions import BadRequest
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar, SingleRecurrence, WeeklyRecurrence
from django.utils.timezone import datetime


class EventResource(DjangoResource):
    # TODO: Need to update fields preparer for recurrence, maybe include type of recurrence
    preparer = FieldsPreparer(fields={
        'id': 'pk',
        'start': 'start',
        'end': 'end',
        'title': 'title',
        'calendar': 'calendar.id',
        'location': 'location',
        'description': 'description',
        'recurrence_type': 'recurrence_type.type',
    })

    # Authentication!
    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/events/
    # Gets a list of events that belong to the current user within a certain time range.
    def list(self):
        errors = defaultdict(list)
        start = self.request.GET.get('range_start', None)
        end = self.request.GET.get('range_end', None)
        event_id = self.request.GET.get('event_id', None)

        if start is not None:
            range_start = datetime.strptime(start, '%Y-%m-%d %H:%M')
        else:
            range_start = datetime.strptime('1990-01-01 12:12', '%Y-%m-%d %H:%M')
        if end is not None:
            range_end = datetime.strptime(end, '%Y-%m-%d %H:%M')
        else:
            range_end = datetime.strptime('2050-01-01 12:12', '%Y-%m-%d %H:%M')
        if errors:
            raise BadRequest(str(errors))

        calendar = self.request.user.profile.calendars.get(title="Default")
        events = calendar.get_between(range_start, range_end)
        if event_id is not None:
            events = calendar.events.get(id=event_id).get_between(range_start, range_end)

        flattened_events = []
        for e in events:
            # TODO try type(e) this except typeerror. if e IS a list, wouldn't it still append? [1, [1]] I'm not sure.
            if type(e) is not list:
                flattened_events.append(e)
            else:
                flattened_events += e
        return flattened_events

    # GET /api/events/<pk>/
    # Gets detail on a specific event.
    def detail(self, pk):
        return Event.objects.get(id=pk, calendar__owner=self.request.user.profile)

    # PUT /api/events/<pk>/
    # Updates some fields on a specified event.
    def update(self, pk):

        # Helper function to shift days_of_week array by some integer offset
        def shift_days(days_of_week, offset):
            prev_days = list(days_of_week)
            next_days = list(days_of_week)
            for i in range(len(days_of_week)):
                next_days[(i + offset) % 7] = prev_days[i]
            return ''.join(next_days)

        event = Event.objects.get(id=pk, calendar__owner=self.request.user.profile)
        errors = defaultdict(list)
        is_recurring = False
        days_diff = 0

        if 'delta_days' in self.data:
            days_diff = self.data['delta_days']

        if 'recurrence_type' in self.data and self.data['recurrence_type'] == 'weekly':
            recurrence = WeeklyRecurrence.objects.get(event=event)
            is_recurring = True
        else:
            recurrence = SingleRecurrence.objects.get(event=event)

        if 'start' in self.data:
            try:
                data_start = datetime.strptime(self.data['start'], '%Y-%m-%d %H:%M')
                if not is_recurring:
                    event.start = data_start
                else:
                    prev_hour = event.start.hour
                    prev_minute = event.start.minute
                    event.start = event.end.replace(hour=data_start.hour, minute=data_start.minute)
                    if prev_hour == 0 and prev_minute == 0:
                        event.start = event.start - timedelta(days=1)

                    event.start = event.start + timedelta(days=days_diff)
                    recurrence.last_event_end = recurrence.last_event_end + timedelta(days=days_diff)

                    recurrence.days_of_week = shift_days(recurrence.days_of_week, days_diff)
                    recurrence.save()
            except ValueError:
                errors['start'].append("Start not in the correct format")

        if 'end' in self.data:
            try:
                data_end = datetime.strptime(self.data['end'], '%Y-%m-%d %H:%M')
                if not is_recurring:
                    event.end = datetime.strptime(self.data['end'], '%Y-%m-%d %H:%M')
                else:
                    event.end = event.end.replace(hour=data_end.hour, minute=data_end.minute)
                    event.end = event.end + timedelta(days=days_diff)
            except ValueError:
                errors['end'].append("End not in the correct format")

        if 'title' in self.data:
            event.title = self.data['title']

        if 'description' in self.data:
            event.description = self.data['description']

        if 'location' in self.data:
            event.location = self.data['location']

        if errors:
            raise BadRequest(str(errors))

        event.save()
        return event

    # POST /api/events/
    # Create an event for the given user.
    def create(self):
        # Error check event fields: calendar, title, start, end
        errors = defaultdict(list)

        start = recurrence_type = days_of_week = frequency = last_event = None
        if 'start' not in self.data:
            errors['start'].append("Start not provided")
        else:
            try:
                start = datetime.strptime(self.data['start'], '%Y-%m-%d %H:%M')
            except ValueError:
                errors['start'].append("Start not in the correct format")

        end = None
        if 'end' not in self.data:
            errors['end'].append("End not provided")
        else:
            try:
                end = datetime.strptime(self.data['end'], '%Y-%m-%d %H:%M')
            except ValueError:
                errors['end'].append("End not in the correct format")

        title = None
        if 'title' not in self.data:
            errors['title'].append("Title not provided")
        else:
            title = self.data['title']

        calendar_title = None
        if 'calendar' not in self.data:
            errors['calendar'].append("Calendar not provided")
        else:
            calendar_title = self.data['calendar']

        # Error check recurrence type
        if 'recurrence_type' not in self.data:
            errors['recurrence_type'].append("Recurrence type not provided")
        elif self.data['recurrence_type'] != 'weekly' and self.data['recurrence_type'] != 'single':
            errors['recurrence_type'].append("recurrence_type not single or weekly")
        else:
            recurrence_type = self.data['recurrence_type']

            # Additional error checks for weekly recurrence
            if recurrence_type == "weekly":
                if 'last_event' not in self.data:
                    errors['last_event'].append("Last event not provided")
                else:
                    try:
                        last_event = datetime.strptime(self.data['last_event'], '%Y-%m-%d %H:%M')
                    except ValueError:
                        errors['last_event'].append("Last_event not in the correct format")

                if 'frequency' not in self.data:
                    errors['frequency'].append("Frequency not provided")
                else:
                    frequency = self.data['frequency']
                    if frequency < 1:
                        errors['frequency'].append("Frequency not valid")

                if 'days_of_week' not in self.data:
                    errors['days_of_week'].append("Days of week not provided")
                else:
                    days_of_week = self.data['days_of_week']
                    # TODO: How to check that the string is of length 7 and all are 0's and 1's?
                    # TODO: If we do error checks here, do we need to error check again in backend?

        if errors:
            raise BadRequest(str(errors))

        event = Event.objects.create(
            start=start,
            end=end,
            title=title,
            calendar=Calendar.objects.get(
                owner=self.request.user.profile,
                title=calendar_title),
            description=self.data.get('description', ''),
            location=self.data.get('location', '')
        )

        if recurrence_type == "single":
            SingleRecurrence.objects.create(
                event=event
            )
        else:
            WeeklyRecurrence.objects.create(
                days_of_week=days_of_week,
                frequency=frequency,
                last_event_end=last_event,
                event=event
            )
        return event

    # DELETE /api/events/<pk>/
    # Deletes a specified event.
    def delete(self, pk):

        Event.objects.get(id=pk, calendar__owner=self.request.user.profile).recurrence_type.delete()
        Event.objects.get(id=pk, calendar__owner=self.request.user.profile).delete()
