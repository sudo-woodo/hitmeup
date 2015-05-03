from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

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

    # Fix me later?
    def is_authenticated(self):
        return True

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
        profile = UserProfile.objects.get(user__id=pk)

        profile.user.email = self.data['email']
        profile.user.first_name = self.data['first_name']
        profile.user.last_name = self.data['last_name']
        profile.user.save()
        profile.save()
        return profile

    # DELETE /api/users/<pk>/
    # Sets a user to inactive with id=pk
    def delete(self, pk):
        profile = UserProfile.objects.get(user__id=pk)
        profile.user.is_active = False
        profile.user.save()


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

    # Fix me later?
    def is_authenticated(self):
        return True

    # GET /api/users/<user>/friends/
    # Gets a list of friends of a user with id=user
    def list(self, user):
        return UserProfile.objects.get(user__id=user).friends

    # PUT /api/users/<user>/friends/<pk>/
    # Adds a friendship of users: 'user' -> 'pk'
    def update(self, user, pk):
        this = UserProfile.objects.get(user__id=user)
        other = UserProfile.objects.get(user__id=pk)

        this.add_friend(other)

    # DELETE /api/users/<user>/friends/<pk>/
    # Removes a friendship of users: 'user <-> 'pk'
    def delete(self, user, pk):
        this = UserProfile.objects.get(user__id=user)
        other = UserProfile.objects.get(user__id=pk)

        this.del_friend(other)
