from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from util.factories import UserFactory
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

HOME_URL = reverse('static_pages:home')
LOGIN_URL = reverse('user_accounts:login')
SEARCH_URL = reverse('search_bar:user_search')
SEARCH_BAR_HTML = 'form id="user-search-form"'
SUGGESTIONS_HTML = 'Search Results'
PROFILE_HTML = 'id="profile-body"'
NO_RESULTS = 'No results found for your query. Try another search item.'
SUGGESTION_FAIL = 'Failed to render suggestions page'
AUTOCOMPLETE_FAIL = 'Suggestions page autocomplete unsuccessful'
NO_RESULT_FAIL = 'Failed to render no results page'

class SearchTestCase(TestCase):
    """
    Tests search implementation.
    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.password = get_random_string()
        self.user = UserFactory(username='TestUser', password=self.password, first_name='Test', last_name='Name')
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }

    def test_search_loggedout(self):
        # Tests that the search bar does not show while the user is not logged in
        response = self.client.get(HOME_URL)
        self.assertNotContains(response=response, text=SEARCH_BAR_HTML)

    def test_search_loggedin(self):
        # Tests that the search bar does show while the user is logged in
        self.client.post(LOGIN_URL, self.LOGIN_INFO) # login
        response = self.client.get(HOME_URL)
        self.assertContains(response=response, text=SEARCH_BAR_HTML)

    def test_search_submit(self):
        # Tests that searching an exact match will redirect to the user's profile
        self.client.post(LOGIN_URL, self.LOGIN_INFO) # login
        user1 = UserFactory(username='ThaDoggFather', first_name='Snoop', last_name='Dogg')
        user1.save()
        profile = user1.profile
        profile.save()
        search_response= self.client.get(SEARCH_URL, {'q': 'ThaDoggFather'})
        self.assertEqual(user1.profile, User.objects.get(username=user1.username).profile)
        self.assertEqual(user1.first_name, User.objects.get(username=user1.username).first_name)
        self.assertRedirects(search_response, reverse('user_accounts:user_profile', args=(user1.username,)))

        # Tests that an incomplete query will redirect to a suggested results page
        search_response = self.client.get(SEARCH_URL, {'q': 'ThaD'})
        self.assertContains(search_response, SUGGESTIONS_HTML, msg_prefix=SUGGESTION_FAIL)
        self.assertContains(search_response, 'ThaDoggFather', msg_prefix=AUTOCOMPLETE_FAIL)


        # TODO: To use these tests we need to figure out how to update index in testing. For now they are commented out.

        # Test first name query
        # search_response = self.client.get(SEARCH_URL, {'q': 'Snoop'})
        # self.assertContains(search_response, SUGGESTIONS_HTML, msg_prefix=SUGGESTION_FAIL)
        # self.assertContains(search_response, 'ThaDoggFather', msg_prefix=AUTOCOMPLETE_FAIL)

        # Test last name query
        #search_response = self.client.get(SEARCH_URL, {'q': 'Dogg'})
        #self.assertContains(search_response, SUGGESTIONS_HTML, msg_prefix=SUGGESTION_FAIL)
        #self.assertContains(search_response, 'ThaDoggFather', msg_prefix=AUTOCOMPLETE_FAIL)

        # Test full name query
        # search_response = self.client.get(SEARCH_URL, {'q': 'Snoop Dogg'})
        # self.assertContains(search_response, SUGGESTIONS_HTML, msg_prefix=SUGGESTION_FAIL)
        # self.assertContains(search_response, 'ThaDoggFather', msg_prefix=AUTOCOMPLETE_FAIL)


        # Tests that a no matching query redirects to a "no results" page
        search_response = self.client.get(SEARCH_URL, {'q': 'advjnaol12'})
        self.assertContains(search_response, NO_RESULTS, msg_prefix=NO_RESULT_FAIL)
