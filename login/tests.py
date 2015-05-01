from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

SIGNUP_URL = reverse('login:signup')
LOGIN_URL = reverse('login:login')
HOME_URL = reverse('staticpages:home')
LOGIN_INFO = {'username': 'name', 'password': 'password'}
SIGNUP_INFO = LOGIN_INFO.copy()
SIGNUP_INFO.update({'email': 'email@website.com'})


class SignUpTestCase(TestCase):
    """
    Tests signup implementation.
    """
    def setUp(self):
        self.client = Client()

    def test_standard(self):
        # Tests a standard registering of a new user
        response = self.client.post(SIGNUP_URL, SIGNUP_INFO)
        user = User.objects.get(username=SIGNUP_INFO['username'])

        # Tests the auto login and redirect
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk, "User was not logged in")
        self.assertRedirects(response, HOME_URL)

    def test_existing_user(self):
        # Registers a new user
        self.client.post(SIGNUP_URL, SIGNUP_INFO)

        # Tests registering with the same username
        response = self.client.post(SIGNUP_URL, SIGNUP_INFO)
        self.assertContains(response, 'form-error')

    def test_signup_while_logged_in(self):
        # Tests accessing the signup page while already logged in
        self.client.post(SIGNUP_URL, SIGNUP_INFO)
        self.client.post(LOGIN_URL, LOGIN_INFO)
        response = self.client.get(SIGNUP_URL)
        self.assertRedirects(response, HOME_URL)


class LoginTestCase(TestCase):
    """
    Tests login implementation.
    """
    def setUp(self):
        self.client = Client()
        self.client.post(SIGNUP_URL, SIGNUP_INFO)

    def test_standard(self):
        # Tests a standard logging in of a user
        response = self.client.post(LOGIN_URL, LOGIN_INFO)
        user = User.objects.get(username=LOGIN_INFO['username'])
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk,
                         "User was not logged in")
        self.assertRedirects(response, HOME_URL)

    def test_wrong_user(self):
        # Tests a logging in of a user with incorrect information
        response = self.client.post(LOGIN_URL, {'username': 'Name',
                                                'password': 'wrongpassword'})
        print(response)
        self.assertContains(response, 'form-error')

