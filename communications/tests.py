from django.core import mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils.crypto import get_random_string
from util.factories import UserFactory

SIGNUP_URL = reverse('user_accounts:signup')

class EmailTestCase(TestCase):
    """
    Tests emails.
    """
    def setUp(self):
        self.client = Client()
        self.password = get_random_string()
        self.user = UserFactory.create(password=self.password)
        self.LOGIN_INFO = {
            'username': self.user.username,
            'password': self.password,
        }

    def test_signup(self):
        # make fake signup info
        SIGNUP_INFO = {
            'username': 'X' + self.user.username,
            'password': 'X' + self.password,
            'confirm_password': 'X' + self.password,
            'email': 'X' + self.user.email,
        }

        response = self.client.post(SIGNUP_URL, SIGNUP_INFO)
        user = User.objects.get(username=SIGNUP_INFO['username'])

        # Makes sure test outbox has an email
        self.assertEqual(len(mail.outbox), 1)

        # Checks subject to be welcome subject, to test that welcome email was sent
        self.assertEqual(mail.outbox[0].subject, 'Welcome to HitMeUp!')
