from django.core.urlresolvers import resolve

from config import entries


class NavbarMiddleware:
    def process_template_response(self, request, response):
        # Mark the active view
        active = resolve(request.path).view_name
        nav = entries()
        for entry in nav:
            if entry['view'] == active:
                entry['active'] = True
        response.context_data['nav'] = nav

        return response
