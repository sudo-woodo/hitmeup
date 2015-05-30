from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth.models import *
from user_accounts.models import *

urlpatterns = [
    url(r'^results/$', views.user_search, name='user_search'),
    url(r'^autocomplete/$', views.user_autocomplete, name='user_autocomplete'),
    # url(r'^user/(?P<username>[\w.@+-]+)/$', views.UserProfile.as_view(),
    #     name='user_profile'),
]
