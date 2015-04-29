from django.conf.urls import url
import views

urlpatterns = [
    url(r'^login/$', views.do_login, name='do_login'),
    url(r'^logout/$', views.do_logout, name='do_logout'),
]
