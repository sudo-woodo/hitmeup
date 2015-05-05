from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from ourcalendar.models import Event, Calendar
from user_accounts.models import UserProfile
from django.contrib.auth.models import User

class EventResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'start': 'start',
        'end': 'end',
        'title': 'title',
        'calendar': 'calendar.title',
        'location': 'location',
        'description': 'description',
    })

    # Authentication!
    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/events/
    def list(self):
        return Event.objects.all()

    # GET /api/events/<pk>/
    def detail(self, pk):
        return Event.objects.get(id=pk)

    # POST /api/events/
    def create(self):
        e = Event.objects.create(
            start=self.data['start'],
            end=self.data['end'],
            title=self.data['title'],
            #Get a calendar who's owner profile is linked to the user sending the POST request
            calendar=Calendar.objects.get(
                owner=UserProfile.objects.get(user=self.request.user),
                title=self.data['calendar']),
            description=self.data['description']
        )
        return e