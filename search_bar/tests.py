from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from util.factories import UserFactory
from django.utils.crypto import get_random_string


# TODO: ADD TESTS

HOME_URL = reverse('static_pages:home')
LOGIN_URL = reverse('user_accounts:login')
SEARCH_BAR_HTML = 'form id="user-search-form"'

class SearchTestCase(TestCase):
    """
    Tests search implementation.
    """
    def setUp(self):
        self.client = Client()
        self.password = get_random_string()
        self.user = UserFactory.create(password=self.password)
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }

    def test_navbar_entry_loggedout(self):
        # Tests that the search bar does not show while the user is not logged in
        response = self.client.get(HOME_URL)
        self.assertNotContains(response=response, text=SEARCH_BAR_HTML)

    def test_navbar_entry_loggedin(self):
        # Tests that the search bar does show while the user is logged in
        self.client.post(LOGIN_URL, self.LOGIN_INFO) # login
        response = self.client.get(HOME_URL)
        self.assertContains(response=response, text=SEARCH_BAR_HTML)

    