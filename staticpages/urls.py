from django.conf.urls import url
from django.views.generic import TemplateView
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
