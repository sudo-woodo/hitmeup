from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SyncView.as_view(), name='sync'),
]
