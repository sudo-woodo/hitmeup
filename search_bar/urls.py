from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^results/$', views.UserSearch.as_view(), name='search'),
]
