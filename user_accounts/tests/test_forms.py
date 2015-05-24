from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils.crypto import get_random_string
from util.factories import UserFactory


SIGNUP_URL = reverse('user_accounts:signup')
SIGNUP_EXTENDED_URL = reverse('user_accounts:extended_signup')
SIGNUP_EXTENDED_URL += '?first_visit=true'
LOGIN_URL = reverse('user_accounts:login')
SETTINGS_URL = reverse('user_accounts:settings')
HOME_URL = reverse('static_pages:home')


class SignUpTestCase(TestCase):
    """
    Tests signup implementation.
    """
    def setUp(self):
        self.client = Client()
        self.password = get_random_string()
        self.user = UserFactory.create(password=self.password)
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }

        # make fake signup info
        self.SIGNUP_INFO = {
            'username': 'X' + self.user.username,
            'password': 'X' + self.password,
            'email': 'X' + self.user.email,
        }

    def test_standard(self):
        # Tests a standard registering of a new user
        response = self.client.post(SIGNUP_URL, self.SIGNUP_INFO)
        user = User.objects.get(username=self.SIGNUP_INFO['username'])

        # Tests the auto login and redirect
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk, "User was not logged in")
        self.assertRedirects(response, SIGNUP_EXTENDED_URL)

    def test_existing_user(self):
        # Tests registering with the same username
        response = self.client.post(SIGNUP_URL, self.LOGIN_INFO)
        self.assertContains(response, 'form-error')

    def test_signup_while_logged_in(self):
        # Tests accessing the signup page while already logged in
        self.client.login(**self.LOGIN_INFO)
        response = self.client.get(SIGNUP_URL)
        self.assertRedirects(response, HOME_URL)


class LoginTestCase(TestCase):
    """
    Tests login implementation.
    """
    def setUp(self):
        self.client = Client()
        self.password = get_random_string()
        self.user = UserFactory.create(password=self.password)
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }
        self.INCORRECT_LOGIN_INFO = {
            'username': 'X' + self.user.username,
            'password': 'X' + self.password,
        }

    def test_standard(self):
        # Tests a standard logging in of a user
        response = self.client.post(LOGIN_URL, self.LOGIN_INFO)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk,
                         "User was not logged in")
        self.assertRedirects(response, HOME_URL)

    def test_wrong_user(self):
        # Tests a logging in of a user with incorrect information
        response = self.client.post(LOGIN_URL, self.INCORRECT_LOGIN_INFO)
        self.assertContains(response, 'form-error')

    def test_login_while_logged_in(self):
        # Tests accessing the signup page while already logged in
        self.client.login(**self.LOGIN_INFO)
        response = self.client.get(LOGIN_URL)
        self.assertRedirects(response, HOME_URL)

class EditSettingsTestCase(TestCase):
    """
    Tests editing settings.
    """
    def setUp(self):
        self.client = Client()
        self.password = get_random_string()

        user = UserFactory.create(password=self.password)
        self.get_user = lambda: User.objects.get(pk=user.pk)

        self.client.login(username=user.username, password=self.password)

    def test_fields(self):
        def assertFields(data, equality):
            assertion = getattr(
                self,
                'assertEqual' if equality else 'assertNotEqual'
            )
            for k, v in data.iteritems():
                if k in {'first_name', 'last_name', 'email'}:
                    assertion(v, getattr(self.get_user(), k))
                else:
                    assertion(v, getattr(self.get_user().profile, k))

        data1 = {
            'first_name': 'Kavin',
            'last_name': 'Smells',
            'email': 'kavinsmells@hitmeup.com',
            'phone': '8888888888',
            'bio': 'I cannot believe how bad I smell.',
        }
        data2 = {k: '0' + v for k, v in data1.iteritems()}
        bad_data = {k: 'X' + v for k, v in data1.iteritems()}

        test_cases = [
            # Change to data1
            {
                'post_data': data1,
                'equality': True,
                'to': data1,
            },

            # Change to data2
            {
                'post_data': data2,
                'equality': True,
                'to': data2,
            },

            # Invalid phone number
            {
                'post_data': bad_data,
                'equality': True,
                'to': data2,
            },
        ]

        for case in test_cases:
            self.client.post(SETTINGS_URL, case['post_data'])
            assertFields(case['to'], case['equality'])


    def test_password(self):
        new_password = 'X' + self.password
        bad_password = 'Y' + self.password
        bad_new_password = 'Z' + self.password

        test_cases = [
            # Success case
            {
                'expected_password': new_password,
                'post_data': {
                    'current_password': self.password,
                    'new_password': new_password,
                }
            },

            # Incorrect password
            {
                'expected_password': new_password,
                'post_data': {
                    'current_password': bad_password,
                    'new_password': bad_new_password,
                }
            },

            # Current not provided
            {
                'expected_password': new_password,
                'post_data': {
                    'new_password': bad_new_password,
                }
            },

            # New not provided
            {
                'expected_password': new_password,
                'post_data': {
                    'current_password': bad_password,
                }
            },

            # New not provided #2
            {
                'expected_password': new_password,
                'post_data': {
                    'current_password': new_password,
                }
            },
        ]

        for case in test_cases:
            self.client.post(SETTINGS_URL, case['post_data'])
            self.assertTrue(check_password(case['expected_password'],
                                           self.get_user().password))
