from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar
from django.utils.html import escape

class EventResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'event_id': 'event.id',
        'start': 'start',
        'end': 'end',
        'title': 'title',
        'calendar': 'calendar.id',
        'location': 'location',
        'description': 'description',
    })
  # POST data fields that are accepted
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
        return Event.objects.get(id=pk)

    # POST /api/events/
    def create(self):
        event = Event.objects.create(
            start=escape(self.data['start']),
            end=escape(self.data['end']),
            title=escape(self.data['title']),
            #Get a calendar who's owner profile is linked to the user sending the POST request
            calendar=Calendar.objects.get(
                owner=escape(self.request.user.profile),
                title=escape(self.data['calendar'])),
            description=escape(self.data['description']),
            location=escape(self.data['location'])
        )
        return event