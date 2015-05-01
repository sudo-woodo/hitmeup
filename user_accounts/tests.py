from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from util import random_string
import factory

SIGNUP_URL = reverse('user_accounts:signup')
LOGIN_URL = reverse('user_accounts:login')
HOME_URL = reverse('static_pages:home')
UserFactory = factory.make_factory(User,
    username=factory.LazyAttribute(lambda _: random_string()),
    password=factory.PostGenerationMethodCall('set_password', random_string()),
    email=factory.LazyAttribute(lambda u: '%s@example.com' % u.username),
)


class SignUpTestCase(TestCase):
    """
    Tests signup implementation.
    """
    def setUp(self):
        self.client = Client()
        self.password = random_string()
        self.user = UserFactory.create(password=self.password)
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }
        self.SIGNUP_INFO = self.LOGIN_INFO.copy()
        self.SIGNUP_INFO.update({
            'email': self.user.email,
        })

    def test_standard(self):
        # Tests a standard registering of a new user
        response = self.client.post(SIGNUP_URL, self.SIGNUP_INFO)
        user = User.objects.get(username=self.SIGNUP_INFO['username'])

        # Tests the auto login and redirect
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk, "User was not logged in")
        self.assertRedirects(response, HOME_URL)

    def test_existing_user(self):
        # Registers a new user
        self.client.post(SIGNUP_URL, self.SIGNUP_INFO)

        # Tests registering with the same username
        response = self.client.post(SIGNUP_URL, self.SIGNUP_INFO)
        self.assertContains(response, 'form-error')

    def test_signup_while_logged_in(self):
        # Tests accessing the signup page while already logged in
        self.client.post(SIGNUP_URL, self.SIGNUP_INFO)
        self.client.post(LOGIN_URL, self.LOGIN_INFO)
        response = self.client.get(SIGNUP_URL)
        self.assertRedirects(response, HOME_URL)


class LoginTestCase(TestCase):
    """
    Tests user_accounts implementation.
    """
    def setUp(self):
        self.client = Client()
        self.password = random_string()
        self.user = UserFactory.create(password=self.password)
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }
        self.INCORRECT_LOGIN_INFO = {
            'username': 'X' + self.user.username,
            'password': 'X' + self.password,
        }

        self.user.save()

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
        self.client.post(LOGIN_URL, self.LOGIN_INFO)
        response = self.client.get(LOGIN_URL)
        self.assertRedirects(response, HOME_URL)
