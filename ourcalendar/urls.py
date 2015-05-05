from django.conf.urls import include, url
import views

from api import EventResource

urlpatterns = [
    # Examples:
    # url(r'^$', 'hitmeup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.calendar, name='view_calendar'),
    url(r'^api/events/$', include(EventResource.urls())),
]
