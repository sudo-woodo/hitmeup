from django.conf import settings
from django.http.response import Http404
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings


NORMAL_ENTRIES = [
    {
        'name': 'Home',
        'view': 'staticpages:home',
    },
    {
        'name': 'About',
        'view': '',
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
        pass

    def test_404(self):
        """
        Tests if 404 requests don't throw errors.
        """
        with self.assertRaises(Http404):
            response = self.client.get('/DOES_NOT_EXIST')

        # ensure no entries are marked active
        for entry in response.context.entries:
            self.assertFalse('active' in entry)

    @override_settings(NAVBAR_ENTRIES=None)
    def test_unset(self):
        """
        Tests if the NAVBAR_ENTRIES setting is unset.
        """
        # unset
        del settings.NAVBAR_ENTRIES

        response = self.client.get('/')
        self.assertFalse(response.context and 'navbar_entries' in response.context, "Found navbar_entries in context.")
