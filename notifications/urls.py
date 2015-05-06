from django.conf.urls import patterns, url, include

from api import NotificationResource
import views

urlpatterns = patterns[
    url(r'^$', views.list, name='list'),
    url(r'^api/$', include(NotificationResource.urls())),
]