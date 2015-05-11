import copy
from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings


def navbar(request):
    """
    Fills the 'navbar_entries' variable with the navbar entries, and marks the active view.
    Will grab the entries from settings.NAVBAR_ENTRIES, in the following format:
    [
        {
            'name': string,
            'view': string,
            'auth_required': bool,
        },
        ...
    ]

    :param request: The request object.
    :return: The dict {'navbar_entries': dict}.
    """

    # Get navbar config
    entries = copy.deepcopy(getattr(settings, 'NAVBAR_ENTRIES', []))
    auth_entries = {
        navbar_entries: entries[navbar_entries]
        for navbar_entries in navbar_entries
        if entries[navbar_entries]['auth_required'] and
        request.user.is_authenticated()
    }
    # Mark the active view
    try:
        active = resolve(request.path).view_name
        for entry in entries:
            entry['active'] = entry['view'] == active
    except Resolver404:
        active = None

    return {'navbar_entries': entries, 'view': active}
