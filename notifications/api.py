from django.utils.html import escape
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer


class NotificationResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'image': 'image_url',
        'action': 'action_url',
        'text': 'text',
        'time': 'natural_time',
        'read': 'read',
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/notifications/
    def list(self):
        return self.request.user.profile.notifications.all()

    # GET /api/notifications/<pk>/
    def detail(self, pk):
        return self.request.user.profile.notifications.get(id=pk)

    # PUT /api/notifications/<pk>/
    def update(self, pk):
        notification = self.request.user.profile.notifications.get(id=pk)
        notification.read = escape(self.data['read'])

        notification.save()
        return notification
