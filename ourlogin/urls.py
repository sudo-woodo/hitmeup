from django.conf.urls import url
from django.views.generic import TemplateView
import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.do_login, name='login'),
    url(r'^logout/$', views.do_logout, name='logout'),
]
