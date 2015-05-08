from django.contrib.humanize.templatetags.humanize import naturaltime
from django.test import TestCase
from django.utils import timezone
from notifications.models import Notification
from util.factories import NotificationFactory


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
