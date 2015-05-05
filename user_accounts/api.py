from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import Unauthorized

from .models import UserProfile


class UserProfileResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'username': 'username',
        'email': 'email',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'full_name': 'full_name',
        'is_active': 'user.is_active',
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
    def detail(self, pk):
        return UserProfile.objects.get(user__id=pk)

    # PUT /api/users/<pk>/
    # Updates a user's info with id=pk. Assumes specified user exists,
    # otherwise error is returned.  This is to prevent user creation.
    def update(self, pk):
        if self.request.user.id != int(pk):
            raise Unauthorized('Not authorized to update '
                               'another user\'s profile.')

        profile = UserProfile.objects.get(user__id=pk)

        if 'email' in self.data:
            profile.user.email = self.data['email']
        if 'first_name' in self.data:
            profile.user.first_name = self.data['first_name']
        if 'last_name' in self.data:
            profile.user.last_name = self.data['last_name']
        if 'phone' in self.data:
            profile.phone = self.data['phone']
        if 'bio' in self.data:
            profile.bio = self.data['bio']

        profile.user.save()
        profile.save()
        return profile


class FriendshipResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'username': 'username',
        'email': 'email',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'full_name': 'full_name',
        'is_active': 'user.is_active',
        'bio': 'bio',
        'phone': 'phone',
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/friends/
    # Gets a list of friends of the current user
    def list(self):
        return UserProfile.objects.get(user__id=self.request.user.id).friends

    # PUT /api/friends/<pk>/
    # Adds a friendship of current user -> 'pk'
    def update(self, pk):
        this = UserProfile.objects.get(user__id=self.request.user.id)
        other = UserProfile.objects.get(user__id=pk)
        this.add_friend(other)

    # DELETE /api/friends/<pk>/
    # Removes a friendship of current user <-> 'pk'
    def delete(self, pk):
        this = UserProfile.objects.get(user__id=self.request.user.id)
        other = UserProfile.objects.get(user__id=pk)
        this.del_friend(other)
