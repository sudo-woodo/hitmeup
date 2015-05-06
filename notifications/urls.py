from django.conf.urls import url, include

from api import NotificationResource
import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^api/$', include(NotificationResource.urls())),
]