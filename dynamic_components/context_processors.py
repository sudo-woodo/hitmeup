from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings

def navbar(request):
    # Get navbar config
    try:
        entries = settings.NAVBAR_ENTRIES
    except AttributeError:
        return

    # Mark the active view
    try:
        active = resolve(request.path).view_name
        for entry in entries:
            if entry['view'] == active:
                entry['active'] = True
    except Resolver404:
        pass

    return {'navbar_entries': entries}
