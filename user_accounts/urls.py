from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^edit/$', views.EditView.as_view(), name='edit'),
]
