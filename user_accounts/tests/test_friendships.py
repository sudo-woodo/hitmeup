from django.test.testcases import TestCase
from user_accounts.models import Friendship
from util.factories import UserProfileFactory


class FriendshipTestCase(TestCase):
    NUM_OTHERS = 5

    def setUp(self):
        self.profile = UserProfileFactory()
        self.other = UserProfileFactory()

    def test_add(self):
        # Normal add
        friendship, created = self.profile.add_friend(self.other)
        self.assertFalse(friendship.accepted)
        self.assertTrue(created)

        self.assertEqual(len(self.profile.friends), 0)
        self.assertEqual(len(self.profile.pending_incoming_friends), 0)
        self.assertEqual(len(self.profile.pending_outgoing_friends), 1)

        self.assertEqual(len(self.other.friends), 0)
        self.assertEqual(len(self.other.pending_incoming_friends), 1)
        self.assertEqual(len(self.other.pending_outgoing_friends), 0)

        # Repeat add
        friendship, created = self.profile.add_friend(self.other)
        self.assertFalse(friendship.accepted)
        self.assertFalse(created)

        self.assertEqual(len(self.profile.friends), 0)
        self.assertEqual(len(self.profile.pending_incoming_friends), 0)
        self.assertEqual(len(self.profile.pending_outgoing_friends), 1)

        self.assertEqual(len(self.other.friends), 0)
        self.assertEqual(len(self.other.pending_incoming_friends), 1)
        self.assertEqual(len(self.other.pending_outgoing_friends), 0)

        # Normal accept
        friendship, created = self.other.add_friend(self.profile)
        self.assertTrue(friendship.accepted)
        self.assertTrue(created)

        self.assertEqual(len(self.profile.friends), 1)
        self.assertEqual(len(self.profile.pending_incoming_friends), 0)
        self.assertEqual(len(self.profile.pending_outgoing_friends), 0)

        self.assertEqual(len(self.other.friends), 1)
        self.assertEqual(len(self.other.pending_incoming_friends), 0)
        self.assertEqual(len(self.other.pending_outgoing_friends), 0)

        # Repeat accept
        friendship, created = self.other.add_friend(self.profile)
        self.assertTrue(friendship.accepted)
        self.assertFalse(created)

        self.assertEqual(len(self.profile.friends), 1)
        self.assertEqual(len(self.profile.pending_incoming_friends), 0)
        self.assertEqual(len(self.profile.pending_outgoing_friends), 0)

        self.assertEqual(len(self.other.friends), 1)
        self.assertEqual(len(self.other.pending_incoming_friends), 0)
        self.assertEqual(len(self.other.pending_outgoing_friends), 0)

    def test_del(self):
        # Add friendship
        self.profile.add_friend(self.other)
        self.other.add_friend(self.profile)
        self.assertEqual(len(self.profile.friends), 1)
        self.assertEqual(len(self.other.friends), 1)

        # Delete friendship
        self.profile.del_friend(self.other)
        self.assertEqual(len(self.profile.friends), 0)
        self.assertEqual(len(self.other.friends), 0)
