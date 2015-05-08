from django.conf.urls import include, url
from django.contrib import admin
from django_jinja import views as jinja_views
from api import EventResource


handler400 = jinja_views.BadRequest.as_view()
handler403 = jinja_views.PermissionDenied.as_view()
handler404 = jinja_views.PageNotFound.as_view()
handler500 = jinja_views.ServerError.as_view()

urlpatterns = [
    # Examples:
    # url(r'^$', 'hitmeup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('static_pages.urls', namespace='static_pages')),
    url(r'^', include('user_accounts.urls', namespace='user_accounts')),
    url(r'^calendar/', include('ourcalendar.urls', namespace='calendar')),
    url(r'^api/events/$', include(EventResource.urls()), namespace='events_api'),
]
