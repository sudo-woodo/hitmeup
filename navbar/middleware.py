from django.conf import settings
from django.core.urlresolvers import resolve

class NavbarMiddleware:
    def process_template_response(self, request, response):
        # Mark the active view
        active = resolve(request.path).view_name
        entries = settings.NAVBAR_ENTRIES
        for entry in entries:
            if entry['view'] == active:
                entry['active'] = True
        response.context_data['navbar_entries'] = entries

        return response
