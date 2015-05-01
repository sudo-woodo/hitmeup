from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from login import views as login_views
from staticpages import views as static_views

SIGNUP_URL = reverse(login_views.signup)
LOGIN_URL = reverse(login_views.do_login)
HOME_URL = reverse(static_views.home)

class OurSignUpTestCase(TestCase):
    """
    Tests oursignup implementation.
    """
    def setUp(self):
        self.client = Client()

    def test_standard(self):
        # Tests a standard registering of a new user
        response = self.client.post(SIGNUP_URL, {'username': 'Name', 'password': 'password'})
        user = User.objects.get(username='Name')

        # Tests the auto login and redirect
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk, "User was not logged in")
        self.assertRedirects(response, HOME_URL)

    def test_existingUser(self):
        # Registers a new user
        response = self.client.post(SIGNUP_URL, {'username': 'Name', 'password': 'password'})

        # Tests registering with the same username
        response = self.client.post(SIGNUP_URL, {'username': 'Name', 'password': 'password'})
        self.assertContains(response,
                            '<div class="alert alert-warning alert-dismissible" role="alert">\
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
                            <span aria-hidden="true">&times;</span></button>\
                            Username already exists!</div>', 1, html=True)

    def test_signupWhileLoggedIn(self):
        # Tests accessing the signup page while already logged in
        self.client.post(SIGNUP_URL, {'username': 'Name', 'password': 'password'})
        self.client.post(LOGIN_URL, {'username': 'Name', 'password': 'password'})
        response = self.client.get(SIGNUP_URL)
        self.assertRedirects(response, HOME_URL)


class LoginTestCase(TestCase):
    """
    Tests login implementation.
    """
    def setUp(self):
        self.client = Client()
        self.client.post(SIGNUP_URL, {'username': 'Name', 'password': 'password'})

    def test_standard(self):
        # Tests a standard logging in of a user
        response = self.client.post(LOGIN_URL, {'username': 'Name', 'password': 'password'})
        user = User.objects.get(username='Name')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk, "User was not logged in")
        self.assertRedirects(response, HOME_URL)

    def test_wrongUser(self):
        # Tests a logging in of a user with incorrect information
        response = self.client.post(LOGIN_URL, {'username': 'Name', 'password': 'wrongpassword'})

        self.assertContains(response,
                            '<div class="alert alert-danger alert-dismissible" role="alert">\
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
                            <span aria-hidden="true">&times;</span></button>\
                            Invalid username or password</div>', 1, html=True)

