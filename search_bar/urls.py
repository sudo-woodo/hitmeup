from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^search/$', views.SearchBase, name='searchbase'),
    url(r'^searchresults/$', views.Search.as_view(), name='search'),
]