from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings


class NavbarMiddleware:
    def process_response(self, request, response):
        entries = settings.NAVBAR_ENTRIES

        # Mark the active view
        try:
            active = resolve(request.path).view_name
            for entry in entries:
                if entry['view'] == active:
                    entry['active'] = True
        except Resolver404:
            pass

        # Set the navbar
        # TODO: add context to 404/etc handlers?
        try:
            response.context_data['navbar_entries'] = entries
        except AttributeError:
            response.context_data = {
                'navbar_entries': entries
            }

        return response
