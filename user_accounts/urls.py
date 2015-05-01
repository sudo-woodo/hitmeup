from django.conf.urls import url
from user_accounts import views

urlpatterns = [
    url(r'^signup/$', views.do_signup, name='signup'),
    url(r'^login/$', views.do_login, name='login'),
    url(r'^logout/$', views.do_logout, name='logout'),
]
