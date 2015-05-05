from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from notifications.models import Notification


class NotificationResource(DjangoResource):
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
        return self.request.user.is_authenticated()
        #return True

    # GET /api/events/
    #TODO LIST GET
    def list(self):
        return Notification.objects.all()

    # GET /api/events/<pk>/
    def detail(self, pk):
        return Notification.objects.get(id=pk)

    #TODO DETAIL PUT

    # PUT /api/posts/<pk>/
    def update(self, pk):
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            post = Notification()

        notification.title = self.data['title']
        notification.user = User.objects.get(username=self.data['author'])
        notification.content = self.data['body']
        notification.save()
        return post