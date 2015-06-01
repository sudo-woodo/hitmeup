from django.contrib.auth import *
from user_accounts.models import UserProfile
from django.http import *
from django.core.handlers.wsgi import WSGIRequest

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
            print("shouldn't run")
            fb_id = response.get('id')
            profile = UserProfile.objects.filter(fb_id=fb_id)

            if profile.count():
               user = authenticate(token=fb_id)
               login(backend.strategy.request, user)

            #TODO hash not in db yet, prompt if they want to make account