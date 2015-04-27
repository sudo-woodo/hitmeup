from datetime import datetime, timedelta
import json
import requests
from django.shortcuts import render


def login(request):
    user = request.user
    if user.is_authenticated():
        social = user.social_auth.get(provider='google-oauth2')
        params = {
           'access_token': social.extra_data['access_token'],
        }
        response = requests.post(
            'https://www.googleapis.com/calendar/v3/users/me/calendarList',
            params=params,
        )
        data = response.json()
    else:
        data = None
        params = None

    return render(request, 'google_login/login.jinja', {
        'ext_js': [
            'https://apis.google.com/js/platform.js'
        ],
        'data': data,
        'params': params,
    })