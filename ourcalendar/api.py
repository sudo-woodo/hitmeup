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
        'event': ['start', 'end', 'location', 'description'],
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
        event = Event.objects.get(id=pk)
        #TODO How to check if data['start'] was in request
        event.start=escape(self.data['start']),
        event.end=escape(self.data['end']),
        event.title = escape(self.data['title']),
        event.description = escape(self.data['description']),
        event.location = escape(self.data['location'])
        return event

    # POST /api/events/
    def create(self):
        errors = defaultdict(list)
        if 'start' not in self.data:
            errors['start'].append("Not provided")
        else:
            try:
                start = datetime.strptime(escape(self.data['start']), '%Y-%m-%d %H:%M')
            except ValueError:
                errors['start'].append("Not in the correct format")

        if errors:
            raise BadRequest(str(errors))

        event = Event.objects.create(
            start=start,
            end=datetime.strptime(escape(self.data['end']), "%Y-%m-%d %H:%M"),
            title=escape(self.data['title']),
            # Get a calendar whose owner profile is linked to the user
            # sending the POST request
            calendar=Calendar.objects.get(
                owner=self.request.user.profile,
                title=escape(self.data['calendar'])),
            description=escape(self.data['description']),
            location=escape(self.data['location'])
        )
        return event