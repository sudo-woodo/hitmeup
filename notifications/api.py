from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from notifications.models import Notification
from user_accounts.models import UserProfile


class NotificationResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'user': 'user',
        'image_url': 'image_url',
        'action_url': 'action_url',
        'text': 'text',
        'read': 'read',
    })

    # Authentication!
    def is_authenticated(self):
        # Open everything wide!
        # DANGEROUS, DO NOT DO IN PRODUCTION.
        #return self.request.user.is_authenticated()
        return True

    # GET /api/
    #TODO LIST GET
    def list(self):
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