from django.core import mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils.crypto import get_random_string
from util.factories import UserFactory

class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail('Test email', 'The test email was successfully sent!',
            'sudowoodohitmeup@gmail.com@', ['sudowoodohitmeup@gmail.com'],
            fail_silently=False)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Test email')


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

    def test_standard_email_sent(self):
        # Tests a standard registering of a new user
        response = self.client.post(SIGNUP_URL, self.SIGNUP_INFO)
        user = User.objects.get(username=self.SIGNUP_INFO['username'])

        # Makes sure test outbox has an email
        self.assertEqual(len(mail.outbox), 1)
        #checks subject to be welcome subject, to test that welcome email was sent
        self.assertEqual(mail.outbox[0].subject, 'Welcome to HitMeUp!')

    def test_existing_user(self):
        # Tests registering with the same username
        response = self.client.post(SIGNUP_URL, self.LOGIN_INFO)
        #test that no email was sent
        self.assertEqual(len(mail.outbox), 0)

    def test_signup_while_logged_in(self):
        # Tests accessing the signup page while already logged in
        self.client.login(**self.LOGIN_INFO)
        response = self.client.get(SIGNUP_URL)
        #test that no email was sent
        self.assertEqual(len(mail.outbox), 0)

