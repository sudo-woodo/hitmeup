from collections import defaultdict
from restless.dj import DjangoResource
from restless.exceptions import BadRequest
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar
from django.utils.html import escape
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

    # POST data fields that are accepted
    # TODO use this!
    MODIFIABLE_FIELDS = {
        'event': ['start', 'end', 'location', 'description', 'title'],
    }

    # Authentication!
    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/events/
    def list(self):
        return Event.objects.filter(calendar__owner=self.request.user.profile)

    # GET /api/events/<pk>/
    def detail(self, pk):
        return Event.objects.get(id=pk, calendar__owner=self.request.user.profile)

    # PUT /api/events/<pk>/
    def update(self, pk):
        event = Event.objects.get(id=pk, calendar__owner=self.request.user.profile)
        #TODO How to check if data['start'] was in request

        errors = defaultdict(list)

        if 'start' in self.data:
            try:
                event.start = datetime.strptime(escape(self.data['start']), '%Y-%m-%d %H:%M')
            except ValueError:
                errors['start'].append("Start not in the correct format")

        if 'end' in self.data:
            try:
                event.end = datetime.strptime(escape(self.data['end']), '%Y-%m-%d %H:%M')
            except ValueError:
                errors['end'].append("End not in the correct format")

        if 'title' in self.data:
            event.title = escape(self.data['title'])

        if 'description' in self.data:
            event.description = escape(self.data['description'])

        if 'location' in self.data:
            event.location = escape(self.data['location'])

        event.save()

        return event

    # POST /api/events/
    def create(self):
        #Error check calendar, title, start, end
        errors = defaultdict(list)
        if 'start' not in self.data:
            errors['start'].append("Start not provided")
        else:
            try:
                start = datetime.strptime(escape(self.data['start']), '%Y-%m-%d %H:%M')
            except ValueError:
                errors['start'].append("Start not in the correct format")

        if 'end' not in self.data:
            errors['end'].append("End not provided")
        else:
            try:
                end = datetime.strptime(escape(self.data['end']), '%Y-%m-%d %H:%M')
            except ValueError:
                errors['end'].append("End not in the correct format")

        if 'title' not in self.data:
            errors['title'].append("Title not provided")
        else:
            title=escape(self.data['title'])

        if 'calendar' not in self.data:
            errors['calendar'].append("Calendar not provided")
        else:
            calendarName=escape(self.data['calendar'])

        if errors:
            raise BadRequest(str(errors))

        event = Event.objects.create(
            start=start,
            end=end,
            title=title,
            # Get a calendar whose owner profile is linked to the user
            # sending the POST request
            calendar=Calendar.objects.get(
                owner=self.request.user.profile,
                title=calendarName),
            description=escape(self.data['description']),
            location=escape(self.data['location'])
        )
        return event