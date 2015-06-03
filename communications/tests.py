from django.core import mail
from django.test import TestCase, Client
from util.factories import *
from user_accounts.models import *

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

    def test_notification(self):
        # testing notification emails for sending friend requests
        users = [UserProfileFactory(user__email='sudowoodohitmeup@gmail.com') for _ in range(3)]
        num_mails = 0

        for f1 in users:
            for f2 in users:
                if f1 is not f2:
                    f1.add_friend(f2)
                    self.assertEqual(mail.outbox[num_mails].subject,
                                     'A Notification from HitMeUp')
                    num_mails += 1
                    self.assertEqual(len(mail.outbox), num_mails)

        # No repeat notifs
        for f1 in users:
            for f2 in users:
                if f1 is not f2:
                    f1.add_friend(f2)
                    self.assertEqual(len(mail.outbox), num_mails)
