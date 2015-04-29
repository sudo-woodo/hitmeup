from datetime import datetime, timedelta
import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
import requests
from django.shortcuts import render


def do_login(request):
    user = request.user
    if user.is_authenticated():
        social = user.social_auth.get(provider='google-oauth2')
        params = {
            'access_token': social.access_token,
        }
        response = requests.get(
            'https://www.googleapis.com/calendar/v3/calendars/%s/events' % 'metakirby5@gmail.com',
            params=params,
        )
        resp = response.json()
    else:
        resp = None

    return render(request, 'google_login/login.jinja', {
        'ext_js': [
            'https://apis.google.com/js/platform.js'
        ],
        'resp': resp,
    })

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('google_login:do_login'))
