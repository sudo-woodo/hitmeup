from django.contrib.humanize.templatetags.humanize import naturaltime
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.utils.crypto import get_random_string
from notifications.models import Notification
from util.factories import NotificationFactory, UserFactory


class ModelTestCase(TestCase):
    """
    Tests if signals actually create models.
    """
    def test_ordering(self):
        # Tests if models are ordered correctly.
        t0 = timezone.now()
        t1 = t0 + timezone.timedelta(hours=1)
        n0 = NotificationFactory(time=t0)
        n1 = NotificationFactory(time=t1)

        self.assertEqual(n0, Notification.objects.all()[1],
                         "Earlier notification not last")
        self.assertEqual(n1, Notification.objects.all()[0],
                         "Later notification not first")

    def test_attrs(self):
        # Tests if attributes are set correctly.
        t = timezone.now()
        n = NotificationFactory(time=t)

        self.assertEqual(n.natural_time, naturaltime(t))

class ApiTestCase(TestCase):
    """
    Tests the REST API.
    """
    def setUp(self):
        # set up notifs
        self.multi_user_notifs = [NotificationFactory() for _ in range(5)]

        password = get_random_string()
        user = UserFactory(password=password)
        self.profile = user.profile
        self.single_user_notifs = [
            NotificationFactory(recipient=self.profile) for _ in range(5)
        ]

        # set up clients
        self.anon_client = Client()
        self.auth_client = Client()
        self.auth_client.login(username=user.username,
                               password=password)

    def test_auth(self):
        pass
