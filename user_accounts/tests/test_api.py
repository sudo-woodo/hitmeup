import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.crypto import get_random_string
from user_accounts.models import UserProfile
from util.factories import UserFactory


class ApiTestCase(TestCase):

    NUM_USERS = 5
    FRIENDS_LIST_URL = reverse('friends_api:api_friend_list')
    FRIENDS_GET_DETAIL_URL = lambda self, pk: reverse(
        'friends_api:api_friend_detail', args=[pk])

    def setUp(self):
        # Create lots of dummy users
        self.all_users = [UserFactory(password=get_random_string())
                          for _ in range(self.NUM_USERS - 1)]

        # Pick one user for main testing
        password = get_random_string()
        user = UserFactory(password=password)
        self.profile = user.profile
        self.all_users.append(user)

        # Set up client
        self.client = Client()
        self.client.login(username=user.username,
                          password=password)

    def test_auth(self):
        # Tests if request rejected when not authenticated
        anon_client = Client()
        response = anon_client.get(self.FRIENDS_LIST_URL)
        self.assertEqual(response.status_code, 401)
        response = anon_client.get(self.FRIENDS_GET_DETAIL_URL(
            UserFactory().pk
        ))
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Tests if list api works
        response = self.client.get(self.FRIENDS_LIST_URL)
        print self.FRIENDS_LIST_URL, json.loads(response.content)
        data = json.loads(response.content)['objects']

        # Initially, user should have no friends :(
        self.assertEqual(len(data), 0)