from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^signup/extended/$', views.SignUpExtended.as_view(),
        name='extended_signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^settings/$', login_required(views.SettingsView.as_view()),
        name='settings'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.UserProfile.as_view(),
        name='user_profile')
]
