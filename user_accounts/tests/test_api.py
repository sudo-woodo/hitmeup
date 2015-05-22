import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.crypto import get_random_string
from user_accounts.models import UserProfile, Friendship
from util.factories import UserFactory


class UserProfilesApiTestCase(TestCase):
    NUM_USERS = 5
    LIST_URL = reverse('users_api:api_userprofile_list')
    GET_DETAIL_URL = lambda self, pk: reverse(
        'users_api:api_userprofile_detail', args=[pk])
    NEW_DATA = {
        'phone': '25411142056',
        'bio': 'I am an attack helicopter.',
        'email': 'snoop@sdsu.edu',
        'first_name': 'Snoop',
        'last_name': 'Dogg',
    }

    def setUp(self):
        # Create lots of dummy users
        self.other_users = [UserFactory(password=get_random_string())
                            for _ in range(self.NUM_USERS)]

        # Pick one user for main testing
        password = get_random_string()
        user = UserFactory(password=password)
        self.profile = user.profile

        # Set up client
        self.client = Client()
        self.client.login(username=user.username,
                          password=password)

    def test_auth(self):
        # Tests if request rejected when not authenticated
        anon_client = Client()
        response = anon_client.get(self.LIST_URL)
        self.assertEqual(response.status_code, 401)
        response = anon_client.get(self.GET_DETAIL_URL(
            UserFactory().pk
        ))
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Tests if list api works
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']

        # Check if we see all the users
        self.assertEqual(len(data), self.NUM_USERS + 1)
        user_ids = [user.id for user in self.other_users]
        user_ids.append(self.profile.pk)
        for user in data:
            self.assertIn(user['id'], user_ids)

        # Make current user inactive
        self.profile.user.is_active = False
        self.profile.user.save()

        # Ensure user not in returned list
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), self.NUM_USERS)
        for user in data:
            self.assertNotEqual(user['id'], self.profile.pk)

    def test_detail(self):
        # Tests if we can get info on the current user
        response = self.client.get(self.GET_DETAIL_URL(self.profile.pk))
        data = json.loads(response.content)

        expected_fields = ['id', 'username', 'email', 'first_name', 'last_name',
                           'full_name', 'bio', 'phone', 'gravatar_url']

        # Ensure all the fields are present
        for field in expected_fields:
            if field == 'id':
                self.assertEqual(data[field], self.profile.pk)
            else:
                self.assertEqual(data[field], getattr(self.profile, field))

        for field in data:
            if field not in expected_fields:
                self.fail("Found unexpected field in data: %s" % field)

    def test_update(self):
        # Try updating another user's profile
        response = self.client.put(self.GET_DETAIL_URL(self.other_users[0].pk),
                                   json.dumps({'bio': self.NEW_DATA['bio']}))

        # Ensure we are unauthorized to do so, and field is unchanged
        self.assertEqual(response.status_code, 401)
        self.assertNotEqual(self.other_users[0].profile.bio, self.NEW_DATA['bio'])

        # Try updating self's profile
        response = self.client.put(self.GET_DETAIL_URL(self.profile.pk),
                                   json.dumps(self.NEW_DATA))
        data = json.loads(response.content)

        for field in self.NEW_DATA:
            self.assertEqual(data[field], self.NEW_DATA[field])
            self.assertEqual(
                getattr(UserProfile.objects.get(pk=self.profile.pk), field),
                self.NEW_DATA[field])


class FriendsApiTestCase(TestCase):
    NUM_USERS = 5
    LIST_URL = reverse('friends_api:api_friend_list')
    GET_DETAIL_URL = lambda self, pk: reverse(
        'friends_api:api_friend_detail', args=[pk])

    def setUp(self):
        # Create lots of dummy users
        self.other_users = [UserFactory() for _ in range(self.NUM_USERS)]

        # Pick one user for main testing
        password = get_random_string()
        user = UserFactory(password=password)
        self.profile = user.profile

        # Set up client
        self.client = Client()
        self.client.login(username=user.username,
                          password=password)

    def test_auth(self):
        # Tests if request rejected when not authenticated
        anon_client = Client()
        response = anon_client.get(self.LIST_URL)
        self.assertEqual(response.status_code, 401)
        response = anon_client.get(self.GET_DETAIL_URL(
            UserFactory().pk
        ))
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Tests if list api works
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']

        # Initially, user should have no friends :(
        self.assertEqual(len(data), 0)

        # Send everyone a friend request
        for user in self.other_users:
            self.profile.add_friend(user.profile)

        # Should still have no friends listed
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), 0)

        # And should have no incoming friendships
        response = self.client.get(self.LIST_URL + '?type=incoming')
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), 0)

        # But should have correct number of outgoing friendships
        response = self.client.get(self.LIST_URL + '?type=outgoing')
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), self.NUM_USERS)

        # Everyone sends us a friend request (so popular!)
        for user in self.other_users:
            user.profile.add_friend(self.profile)

        # Should have correct number of friends listed
        response = self.client.get(self.LIST_URL)
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), self.NUM_USERS)

        # But should have no more outgoing friendships
        response = self.client.get(self.LIST_URL + '?type=outgoing')
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), 0)

    def test_list_incoming(self):
        # Everyone sends us a friend request (so popular!)
        for user in self.other_users:
            user.profile.add_friend(self.profile)

        # Should have correct number of incoming friendships
        response = self.client.get(self.LIST_URL + '?type=incoming')
        data = json.loads(response.content)['objects']
        self.assertEqual(len(data), self.NUM_USERS)

    def test_detail_accepted(self):
        # Become friends with a user
        other = self.other_users[0]
        self.profile.add_friend(other.profile)
        other.profile.add_friend(self.profile)

        # Test that we can get that user's info correctly
        response = self.client.get(self.GET_DETAIL_URL(other.id))
        data = json.loads(response.content)
        for field in data:
            if field == 'accepted' or field == 'favorite':
                friendship = Friendship.objects.get(from_friend=self.profile,
                                                    to_friend=other.profile)
                self.assertEqual(data[field], getattr(friendship, field))
                continue
            elif field == 'id':
                self.assertEqual(data[field], other.pk)
            else:
                attr = getattr(other.profile, field)
                self.assertEqual(data[field], attr)

    def test_detail_unaccepted(self):
        # Get a random user
        other = self.other_users[0]

        # Test that we CAN'T get that user's info
        response = self.client.get(self.GET_DETAIL_URL(other.id))
        data = json.loads(response.content)

        # Ensure 404 is raised and error is returned
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

        # Even if the other user adds us as friend
        other.profile.add_friend(self.profile)

        # Test that we CAN'T get that user's info
        response = self.client.get(self.GET_DETAIL_URL(other.id))
        data = json.loads(response.content)

        # Ensure 404 is raised and error is returned
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_create_detail(self):
        # Add another random user as friend
        other = self.other_users[0]
        response = self.client.post(self.GET_DETAIL_URL(other.id),
                                    content_type='text/json')
        data = json.loads(response.content)

        self.assertFalse(data['accepted'])
        self.assertEqual(data['id'], other.profile.pk)

        # Now, have the other user accept the friend request
        other.profile.add_friend(self.profile)
        self.assertTrue(Friendship.objects.get(
            from_friend=self.profile, to_friend=other.profile).accepted)

    def test_create_detail_add_yourself(self):
        # Add self as friend (such loneliness)
        response = self.client.post(self.GET_DETAIL_URL(self.profile.pk),
                                    content_type='text/json')
        data = json.loads(response.content)

        # Ensure 500 is raised and error is returned
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)

    def test_update(self):
        # Make friendship (self -> random user)
        other = self.other_users[0]
        self.profile.add_friend(other.profile)

        # Test modifying favorite status of unaccepted friendship
        response = self.client.put(self.GET_DETAIL_URL(
            other.profile.pk), json.dumps({'favorite': False}))
        self.assertEqual(response.status_code, 401)

        # Accept the friend request
        other.profile.add_friend(self.profile)

        # Initially, both friendships will be not favorite
        friendship_to = Friendship.objects.get(from_friend=self.profile,
                                               to_friend=other.profile)
        friendship_from = Friendship.objects.get(from_friend=other.profile,
                                                 to_friend=self.profile)
        self.assertFalse(friendship_to.favorite)
        self.assertFalse(friendship_from.favorite)

        # Update with 'favorite' not a bool -> should not update
        response = self.client.put(self.GET_DETAIL_URL(
            other.profile.pk), json.dumps({'favorite': 'True'}))
        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Friendship.objects.get(from_friend=self.profile,
                                   to_friend=other.profile).favorite)

        # Update with 'favorite' missing from data -> should not update
        response = self.client.put(self.GET_DETAIL_URL(
            other.profile.pk), json.dumps({}))
        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Friendship.objects.get(from_friend=self.profile,
                                   to_friend=other.profile).favorite)

        # Try update 'favorite' of another user -> should get error
        response = self.client.put(self.GET_DETAIL_URL(
            self.other_users[1].profile.pk), json.dumps({'favorite': True}))
        self.assertEqual(response.status_code, 404)

        # Set friendship (self -> other) to favorite
        response = self.client.put(self.GET_DETAIL_URL(
            other.profile.pk), json.dumps({'favorite': True}))
        data = json.loads(response.content)

        # Make sure returned data shows favorite as true
        self.assertTrue(data['favorite'])

        # Check 'to' friendship has updated (and 'from' not updated)
        friendship_to = Friendship.objects.get(from_friend=self.profile,
                                               to_friend=other.profile)
        friendship_from = Friendship.objects.get(from_friend=other.profile,
                                                 to_friend=self.profile)
        self.assertTrue(friendship_to.favorite)
        self.assertFalse(friendship_from.favorite)

    def test_delete(self):
        # Make friendship with a random user
        other = self.other_users[0]
        other.profile.add_friend(self.profile)
        self.profile.add_friend(other.profile)

        # Break up with said user
        self.client.delete(self.GET_DETAIL_URL(other.profile.pk))

        # Check if both friendships have been deleted
        with self.assertRaises(Friendship.DoesNotExist):
            Friendship.objects.get(from_friend=self.profile,
                                   to_friend=other.profile)
        with self.assertRaises(Friendship.DoesNotExist):
            Friendship.objects.get(from_friend=other.profile,
                                   to_friend=self.profile)

        # Try deleting friendship again
        self.client.delete(self.GET_DETAIL_URL(other.profile.pk))

        # Check if both friendships are still deleted
        with self.assertRaises(Friendship.DoesNotExist):
            Friendship.objects.get(from_friend=self.profile,
                                   to_friend=other.profile)
        with self.assertRaises(Friendship.DoesNotExist):
            Friendship.objects.get(from_friend=other.profile,
                                   to_friend=self.profile)