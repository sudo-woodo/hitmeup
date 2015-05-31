from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.fb, name='sudowoodo_login_fb'),
    #url(r'^$', 'fb_login.views.home', name='home'),
]