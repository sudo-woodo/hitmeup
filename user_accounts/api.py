from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from .models import UserProfile


class UserProfileResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'username': 'user.username',
        'email': 'user.email',
        'first_name': 'user.first_name',
        'last_name': 'user.last_name',
    })

    # Fix me later?
    def is_authenticated(self):
        return True

    def list(self):
        return UserProfile.objects.filter(user__is_active=True)

    def detail(self, pk):
        return UserProfile.objects.get(user__id=pk)

    def update(self, pk):
        try:
            user = UserProfile.objects.get(user__id=pk)
        except UserProfile.DoesNotExist:
            user = UserProfile()

        user.user.email = self.data['email']
        user.user.first_name = self.data['first_name']
        user.user.last_name = self.data['last_name']
        user.user.save()
        user.save()
        return user

    def delete(self, pk):
        user = UserProfile.objects.get(user__id=pk)
        user.user.is_active = False
        user.user.save()


class FriendshipResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'username': 'user.username',
        'email': 'user.email',
        'first_name': 'user.first_name',
        'last_name': 'user.last_name',
    })

    # Fix me later?
    def is_authenticated(self):
        return True

    def list(self, user):
        return UserProfile.objects.get(user__id=user).friends

    def update(self, user, pk):
        this = UserProfile.objects.get(user__id=user)
        other = UserProfile.objects.get(user__id=pk)

        this.add_friend(other)

    def delete(self, user, pk):
        this = UserProfile.objects.get(user__id=user)
        other = UserProfile.objects.get(user__id=pk)

        this.del_friend(other)
