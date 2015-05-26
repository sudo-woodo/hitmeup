from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^results/$', views.user_search, name='user_search'),
    url(r'^autocomplete/$', views.user_autocomplete, name='user_autocomplete'),
]
