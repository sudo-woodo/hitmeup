import copy
from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings

#TODO documentation
def navbar(request):
    # Get navbar config
    entries = copy.deepcopy(getattr(settings, 'NAVBAR_ENTRIES', []))

    # Mark the active view
    try:
        active = resolve(request.path).view_name
        for entry in entries:
            entry['active'] = entry['view'] == active
    except Resolver404:
        active = None

    return {'navbar_entries': entries, 'view': active}
