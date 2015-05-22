from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import Unauthorized, BadRequest
from django.utils.html import escape
from .models import UserProfile, Friendship


class UserProfileResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'pk',
        'username': 'username',
        'email': 'email',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'full_name': 'full_name',
        'bio': 'bio',
        'phone': 'phone',
        'gravatar_url': 'gravatar_url',
    })

    # POST data fields that are accepted
    MODIFIABLE_FIELDS = {
        'profile': ['phone', 'bio'],
        'user': ['email', 'first_name', 'last_name'],
    }

    # Authenticate if the user is currently logged in
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
            raise Unauthorized("Not authorized to update "
                               "another user's profile.")

        profile = self.request.user.profile

        # Grab and save all modifiable fields from POST data
        for category in self.MODIFIABLE_FIELDS:
            target = profile
            if category == 'user':
                target = profile.user

            for field in self.MODIFIABLE_FIELDS[category]:
                if field in self.data:
                    setattr(target, field, escape(self.data[field]))

        profile.user.save()
        profile.save()
        return profile


class FriendResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'pk',
        'username': 'username',
        'email': 'email',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'full_name': 'full_name',
        'bio': 'bio',
        'phone': 'phone',
        'favorite': 'favorite',
        'accepted': 'accepted',
        'gravatar_url': 'gravatar_url',
    })

    # Authenticate if the user is currently logged in
    def is_authenticated(self):
        return self.request.user.is_authenticated()

    # GET /api/friends/?type=(accepted|incoming|outgoing)
    # Gets a list of friends of the current user.
    # Returns accepted friends if "type" is not specified.
    def list(self):
        # Set accepted, favorite fields for each friend
        def add_friendship_fields(from_friend, to_friend):
            friendship = Friendship.objects.get(
                from_friend=from_friend,
                to_friend=to_friend)

            # Return the friend (not current user)
            if from_friend == self.request.user.profile:
                return_friend = to_friend
            else:
                return_friend = from_friend

            return_friend.accepted = friendship.accepted
            return_friend.favorite = friendship.favorite
            return return_friend

        list_type = self.request.GET.get('type', 'accepted')

        if list_type == 'incoming':
            return [add_friendship_fields(f, self.request.user.profile)
                    for f in self.request.user.profile.pending_incoming_friends]
        elif list_type == 'outgoing':
            return [add_friendship_fields(self.request.user.profile, f)
                    for f in self.request.user.profile.pending_outgoing_friends]

        return [add_friendship_fields(self.request.user.profile, f)
                for f in self.request.user.profile.friends]

    # GET /api/friends/<pk>/
    # Gets info on a specific user or friend.
    # If no friendship from current user -> 'pk', responds with 404.
    def detail(self, pk):
        other = UserProfile.objects.get(user__id=pk)
        friendship = self.request.user.profile.get_friendship(other)
        other.accepted = friendship.accepted
        other.favorite = friendship.favorite
        return other

    # POST /api/friends/<pk>/
    # Adds a friendship of current user -> 'pk'
    def create_detail(self, pk):
        other = UserProfile.objects.get(user__id=pk)
        friendship, created = self.request.user.profile.add_friend(other)
        other.accepted = friendship.accepted
        other.favorite = friendship.favorite
        return other

    # PUT /api/friends/<pk>/
    # Edits favorite status of friend 'pk'
    # data: {'favorite': boolean}
    def update(self, pk):
        other = UserProfile.objects.get(user__id=pk)
        friendship = self.request.user.profile.get_friendship(other)

        if not friendship.accepted:
            raise Unauthorized("Can't set favorite status of a user "
                               "that isn't a friend.")

        try:
            if isinstance(self.data['favorite'], bool):
                friendship.favorite = self.data['favorite']
            else:
                raise BadRequest("'favorite' is not a boolean.")
        except KeyError:
            raise BadRequest("'favorite' not found in sent data.")

        friendship.save()
        other.accepted = friendship.accepted
        other.favorite = friendship.favorite
        return other

    # DELETE /api/friends/<pk>/
    # Removes a friendship of current user <-> 'pk'
    def delete(self, pk):
        other = UserProfile.objects.get(user__id=pk)
        self.request.user.profile.del_friend(other)