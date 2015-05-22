from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^action/(?P<notification_id>\d+)$', views.action, name='action'),
]
