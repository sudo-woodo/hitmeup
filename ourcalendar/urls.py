from django.conf.urls import include, url
import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'hitmeup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.calendar, name='view_calendar'),

]
