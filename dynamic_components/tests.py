from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from util import random_string


HOME_URL = reverse('static_pages:home')
NORMAL_ENTRIES = [
    {
        'name': random_string(),
        'view': 'static_pages:home',
    },
    {
        'name': random_string(),
        'view': 'static_pages:home',
    },
]


@override_settings(NAVBAR_ENTRIES=NORMAL_ENTRIES)
class NavbarTestCase(TestCase):
    """
    Tests different navbar scenarios.
    """

    def setUp(self):
        self.client = Client()

    def test_normal(self):
        """
        Tests if context contains what is expected.
        """
        response = self.client.get(HOME_URL)
        for entry in NORMAL_ENTRIES:
            node = '<a href="%s">%s</a>' % (reverse(entry['view']), entry['name'])
            self.assertContains(response, node, html=True)

    def test_404(self):
        """
        Tests if 404 requests don't throw errors.
        """
        response = self.client.get('/DOES_NOT_EXIST')
        self.assertEqual(response.status_code, 404)

        # ensure no entries are marked active
        self.assertNotContains(response, '<li class="active">', status_code=404, html=True)

    @override_settings(NAVBAR_ENTRIES=None)
    def test_unset(self):
        """
        Tests if the NAVBAR_ENTRIES setting is unset.
        """
        # unset
        del settings.NAVBAR_ENTRIES

        response = self.client.get(HOME_URL)

        for entry in NORMAL_ENTRIES:
            self.assertNotContains(response, entry['name'])
