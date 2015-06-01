from user_accounts.models import UserProfile
from django.contrib.auth.models import User


class MyBackend(object):

    def authenticate(self, token=None):
        # Check the token and return a User.
        profile = UserProfile.objects.filter(fb_id=token)
        return profile[0].user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None