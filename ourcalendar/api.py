from collections import defaultdict
import itertools
from restless.dj import DjangoResource
from restless.exceptions import BadRequest
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar, SingleRecurrence, WeeklyRecurrence
from django.utils.timezone import datetime


class EventResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'event_id': 'pk',
        'start': 'start',
        'end': 'end',
        'title': 'title',
        'calendar': 'calendar.id',
        'location': 'location',
        'description': 'description',
    })

    # Authentication!
    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/events/
    # Gets a list of events that belong to the current user within a certain time range.
    def list(self):
        errors = defaultdict(list)
        if 'range_start' in self.data:
            range_start = self.data['range_start']
        else:
            errors['range_start'].append("range start not provided")
        if 'range_end' in self.data:
            range_end = self.data['range_end']
        else:
            errors['range_end'].append("range end not provided")
        if errors:
            raise BadRequest(str(errors))

        #return Event.objects.filter(calendar__owner=self.request.user.profile)
        return itertools.chain([c.get_between(range_start, range_end)
                                for c in self.request.user.profile.calendars.all()])

        #return self.request.user.profile.calendars

    # GET /api/events/<pk>/
    # Gets detail on a specific event.
    def detail(self, pk):
        return Event.objects.get(id=pk, calendar__owner=self.request.user.profile)

    # PUT /api/events/<pk>/
    # Updates some fields on a specified event.
    def update(self, pk):
        event = Event.objects.get(id=pk, calendar__owner=self.request.user.profile)
        errors = defaultdict(list)

        # TODO BE ABLE TO CHANGE CALENDAR OF EVENT

        if 'start' in self.data:
            try:
                event.start = datetime.strptime(self.data['start'], '%Y-%m-%d %H:%M')
            except ValueError:
                errors['start'].append("Start not in the correct format")

        if 'end' in self.data:
            try:
                event.end = datetime.strptime(self.data['end'], '%Y-%m-%d %H:%M')
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

        start = None  # set a default for each, so PyCharm doesn't complain
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
        if 'type' not in self.data:
            errors['type'].append("Recurrence type not provided")
        elif self.data['type'] != 'weekly' or self.data['type'] != 'single':
            errors['type'].append("recurrence_type not single or weekly")
        else:
            recurrence_type = self.data['type']

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
                #TODO: How to check that the string is of length 7 and all are 0's and 1's?
                #TODO: If we do error checks here, do we need to error check again in backend?

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

        if recurrence_type == "single": #TODO: can we check string equality like this?
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
        Event.objects.get(id=pk, calendar__owner=self.request.user.profile).delete()
