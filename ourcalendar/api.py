from collections import defaultdict
from restless.dj import DjangoResource
from restless.exceptions import BadRequest
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar
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
    # Gets a list of events that belong to the current user.
    def list(self):
        return Event.objects.filter(calendar__owner=self.request.user.profile)

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
        # Error check calendar, title, start, end
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

        return event

    # DELETE /api/events/<pk>/
    # Deletes a specified event.
    def delete(self, pk):
        Event.objects.get(id=pk, calendar__owner=self.request.user.profile).delete()
