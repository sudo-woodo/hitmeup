from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils.crypto import get_random_string
from util.factories import UserFactory


SIGNUP_URL = reverse('user_accounts:signup')
SIGNUP_EXTENDED_URL = reverse('user_accounts:extended_signup')
SIGNUP_EXTENDED_URL += '?first_visit=true'
LOGIN_URL = reverse('user_accounts:login')
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
    Tests user_accounts implementation.
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
