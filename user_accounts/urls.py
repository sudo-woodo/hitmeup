from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^signup/extended/$', views.SignUpExtended.as_view(),
        name='extended_signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # Settings stuff
    url(r'^settings/profile$', views.profile_settings, name='profile_settings'),
    url(r'^settings/subscriptions$', views.subscription_settings, name='subscription_settings'),
    url(r'^settings/password$', views.password_settings, name='password_settings'),

    url(r'^user/(?P<username>[\w.@+-]+)/$', views.UserProfile.as_view(),
        name='user_profile'),
    url(r'^friends/$', views.friends_list, name='friends_list'),
]
