from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from notifications.models import Notification


class NotificationResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'read': 'read',
    })

    # Authentication!
    def is_authenticated(self):
        #return self.request.user.is_authenticated()
        return True

    # GET /api/
    #TODO LIST GET
    def list(self):
        print 1
        return Notification.objects.all()

    # GET /api/
    def detail(self, pk):
        return Notification.objects.get(id=pk)

    #TODO DETAIL PUT

    # PUT /api/<pk>/
    def update(self, pk):
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            notification = Notification()

        notification.read = self.data['read']
        notification.save()
        return notification