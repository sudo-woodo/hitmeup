import json
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.utils.crypto import get_random_string
from notifications.models import Notification, send_friend_request_notification, \
    send_friend_accept_notification, IMAGE_SIZE
from user_accounts.models import UserProfile
from util.factories import NotificationFactory, UserFactory, UserProfileFactory


class ModelTestCase(TestCase):
    """
    Tests the notification model.
    """
    def test_ordering(self):
        # Tests if models are ordered correctly.
        earlier_time = timezone.now()
        later_time = earlier_time + timezone.timedelta(hours=1)
        earlier_notification = NotificationFactory(time=earlier_time)
        later_notification = NotificationFactory(time=later_time)

        self.assertEqual(earlier_notification, Notification.objects.all()[1],
                         "Earlier notification not last")
        self.assertEqual(later_notification, Notification.objects.all()[0],
                         "Later notification not first")

    def test_attrs(self):
        # Tests if attributes are set correctly.
        time = timezone.now()
        notification = NotificationFactory(time=time)

        self.assertEqual(notification.natural_time, naturaltime(time))

    def test_refresh(self):
        # Tests if refresh works.
        notification = NotificationFactory()
        old_time = notification.time
        notification.read = True

        notification.refresh()
        self.assertFalse(notification.read)
        self.assertNotEqual(old_time, notification.time)

        from_db = Notification.objects.get(id=notification.id)
        self.assertEqual(notification.read, from_db.read)
        self.assertEqual(notification.time, from_db.time)

class SignalTestCase(TestCase):
    """
    Tests if signals actually create notifications.
    """
    def setUp(self):
        self.from_friend = UserProfileFactory.create()
        self.to_friend = UserProfileFactory.create()

    def test_friend_request(self):
        # Tests if the notification is created correctly on calling
        # the request handler
        send_friend_request_notification(UserProfile, self.from_friend,
                                         self.to_friend)

        self.assertEqual(len(self.to_friend.notifications.all()), 1)
        notif = self.to_friend.notifications.all()[0]
        self.assertEqual(notif.recipient, self.to_friend)
        self.assertEqual(notif.image_url, self.from_friend.get_gravatar_url(
            IMAGE_SIZE
        ))
        self.assertEqual(notif.action_url, reverse('user_accounts:user_profile',
                                                   args=(self.from_friend.username,)))
        self.assertEqual(notif.text,
                         Notification.NOTIFICATION_STRINGS[Notification.REQUEST_FRIEND]
                         % self.from_friend)

        # Tests if duplicate notifications are sent
        send_friend_request_notification(UserProfile, self.from_friend,
                                         self.to_friend)
        self.assertEqual(len(self.to_friend.notifications.all()), 1)

    def test_friend_accept(self):
        # Tests if the notification is created correctly on calling
        # the accept handler
        send_friend_accept_notification(UserProfile, self.from_friend,
                                        self.to_friend)

        self.assertEqual(len(self.to_friend.notifications.all()), 1)
        notif = self.to_friend.notifications.all()[0]
        self.assertEqual(notif.recipient, self.to_friend)
        self.assertEqual(notif.image_url, self.from_friend.get_gravatar_url(
            IMAGE_SIZE
        ))
        self.assertEqual(notif.action_url, reverse('user_accounts:user_profile',
                                                   args=(self.from_friend.username,)))
        self.assertEqual(notif.text,
                         Notification.NOTIFICATION_STRINGS[Notification.ACCEPT_FRIEND]
                         % self.from_friend)

        # Tests if duplicate notifications are sent
        send_friend_accept_notification(UserProfile, self.from_friend,
                                        self.to_friend)
        self.assertEqual(len(self.to_friend.notifications.all()), 1)

class ApiTestCase(TestCase):
    """
    Tests the REST API.
    """
    NUM_NOTIFS = 5
    LIST_URL = reverse('notifications_api:api_notification_list')
    GET_DETAIL_URL = lambda self, pk: reverse(
        'notifications_api:api_notification_detail', args=[pk])

    def setUp(self):
        # Set up notifs
        self.other_user_notifs = [NotificationFactory() for _ in range(self.NUM_NOTIFS)]

        password = get_random_string()
        user = UserFactory(password=password)
        self.profile = user.profile
        self.my_user_notifs = [
            NotificationFactory(recipient=self.profile) for _ in range(self.NUM_NOTIFS)
        ]

        # Set up client
        self.client = Client()
        self.client.login(username=user.username,
                               password=password)

    def test_auth(self):
        # Tests if request rejected when not authenticated
        anon_client = Client()
        response = anon_client.get(self.LIST_URL)
        self.assertEqual(response.status_code, 401)
        response = anon_client.get(self.GET_DETAIL_URL(
            self.other_user_notifs[0].id
        ))
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Tests if list api works
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']

        # Make sure we can only see our own notifs
        self.assertEqual(len(data), self.NUM_NOTIFS)
        for notif_data in data:
            notif = Notification.objects.get(id=notif_data['id'])
            # Check if contents match up
            self.assertEqual(notif_data['id'], notif.id)
            # Check if profile matches up
            self.assertEqual(notif.recipient, self.profile)

    def test_detail(self):
        # Tests if detail api works
        # Check my own notif
        my_notif = self.my_user_notifs[0]
        response = self.client.get(self.GET_DETAIL_URL(my_notif.id))
        data = json.loads(response.content)
        self.assertEqual(data['id'], my_notif.id)

        # Check someone else's notif - should 404
        their_notif = self.other_user_notifs[0]
        response = self.client.get(self.GET_DETAIL_URL(their_notif.id))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        # Tests if update api works
        # Set up my_notif
        my_notif = self.my_user_notifs[0]
        my_notif.read = False
        my_notif.save()
        get_my_notif = lambda: Notification.objects.get(id=my_notif.id)

        # Update my own notif - no args
        response = self.client.put(self.GET_DETAIL_URL(get_my_notif().id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(get_my_notif().read, False)

        # Update my own notif - with invalid arg
        response = self.client.put(self.GET_DETAIL_URL(get_my_notif().id),
                                   '{"raed": true}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(get_my_notif().read, False)

        # Update my own notif - with non-bool arg
        response = self.client.put(self.GET_DETAIL_URL(get_my_notif().id),
                                   '{"read": "true"}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(get_my_notif().read, False)

        # Update my own notif - with true arg
        response = self.client.put(self.GET_DETAIL_URL(get_my_notif().id),
                                   '{"read": true}')
        data = json.loads(response.content)
        self.assertEqual(data['id'], get_my_notif().id)
        self.assertEqual(data['read'], get_my_notif().read)
        self.assertEqual(get_my_notif().read, True)

        # Update my own notif - with false arg
        response = self.client.put(self.GET_DETAIL_URL(get_my_notif().id),
                                   '{"read": false}')
        data = json.loads(response.content)
        self.assertEqual(data['id'], get_my_notif().id)
        self.assertEqual(data['read'], get_my_notif().read)
        self.assertEqual(get_my_notif().read, False)

        # Update someone else's notif - should 404
        other_notif = self.other_user_notifs[0]
        get_other_notif = lambda: Notification.objects.get(id=other_notif.id)
        response = self.client.put(self.GET_DETAIL_URL(get_other_notif().id),
                                   '{"read": true}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(get_my_notif().read, False)
