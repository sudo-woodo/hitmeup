from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar


class EventResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'start': 'start',
        'end': 'end',
        'title': 'title',
        'calendar': 'calendar.id',
        'location': 'location',
        'description': 'description',
    })

    # Authentication!
    def is_authenticated(self):
        # Open everything wide!
        # DANGEROUS, DO NOT DO IN PRODUCTION.
        #return self.request.user.is_authenticated()
        return True

    # GET /api/events/
    def list(self):
        return Event.objects.all()

    # GET /api/events/<pk>/
    def detail(self, pk):
        return Event.objects.get(id=pk)

    # POST /api/events/
    def create(self):
        print 33
        e = Event.objects.create(
            start=self.data['start'],
            end=self.data['end'],
            title=self.data['title'],
            calendar=Calendar.objects.get(title="Default"),
            description=self.data['description']
        )
        return e