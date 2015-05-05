from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import Unauthorized
from django.utils.html import escape
from .models import UserProfile, Friendship


class UserProfileResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'username': 'username',
        'email': 'email',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'full_name': 'full_name',
        'bio': 'bio',
        'phone': 'phone',
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/users/
    # Gets a list of all active users
    def list(self):
        return UserProfile.objects.filter(user__is_active=True)

    # GET /api/users/<pk>/
    # Gets info of user with id=pk
    # Requested user must be active.
    def detail(self, pk):
        return UserProfile.objects.get(user__id=pk, user__is_active=True)

    # PUT /api/users/<pk>/
    # Updates a user's info with id=pk. Assumes specified user exists,
    # otherwise error is returned.  This is to prevent user creation.
    # NOTE: for AJAX calls through jQuery, use JSON.stringify on your data
    def update(self, pk):
        if self.request.user.id != int(pk):
            raise Unauthorized('Not authorized to update '
                               'another user\'s profile.')

        profile = UserProfile.objects.get(user__id=pk)

        if 'email' in self.data:
            profile.user.email = escape(self.data['email'])
        if 'first_name' in self.data:
            profile.user.first_name = escape(self.data['first_name'])
        if 'last_name' in self.data:
            profile.user.last_name = escape(self.data['last_name'])
        if 'phone' in self.data:
            profile.phone = escape(self.data['phone'])
        if 'bio' in self.data:
            profile.bio = escape(self.data['bio'])

        profile.user.save()
        profile.save()
        return profile


class FriendshipResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'accepted': 'accepted',
        'from_friend': 'from_friend.id',
        'to_friend': 'to_friend.id',
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/friends/
    # Gets a list of friends of the current user, where friends is:
    # accepted friends + outgoing friend requests + incoming friend requests.
    # No duplicate friendships for accepted friends.
    def list(self):
        return \
            Friendship.objects.filter(from_friend=self.request.user.profile) | \
            Friendship.objects.filter(to_friend=self.request.user.profile,
                                      accepted=False)

    # PUT /api/friends/<pk>/
    # Adds a friendship of current user -> 'pk'
    def update(self, pk):
        other = UserProfile.objects.get(user__id=pk)
        self.request.user.profile.add_friend(other)
        return Friendship.objects.get(from_friend=self.request.user.profile,
                                      to_friend=other)

    # DELETE /api/friends/<pk>/
    # Removes a friendship of current user <-> 'pk'
    def delete(self, pk):
        other = UserProfile.objects.get(user__id=pk)
        self.request.user.profile.del_friend(other)
