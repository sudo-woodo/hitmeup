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
        },
        ...
    ]

    :param request: The request object.
    :return: The dict {'navbar_entries': entries}.
    """

    # Get navbar config
    entries = getattr(settings, 'NAVBAR_ENTRIES', [])

    # Mark the active view
    try:
        active = resolve(request.path).view_name
        for entry in entries:
            if entry['view'] == active:
                entry['active'] = True
    except Resolver404:
        pass

    return {'navbar_entries': entries}
