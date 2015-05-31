from django.contrib.auth import *
from user_accounts.models import UserProfile

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        if user:
            profile = user.profile
            profile.fb_id = response.get('id')
            profile.save()
            print profile.fb_id
        # print user.id

def login_user(backend, user, request, response, *args, **kwargs):
    if backend.name == 'facebook':
        if not user or not user.is_authenticated():
           fb_id = response.get('id')
           profile = UserProfile.objects.filter(fb_id=fb_id)
           if profile.count():
              login(request, profile[0])
