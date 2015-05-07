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
        },
        ...
    ]

    :param request: The request object.
    :return: The dict {'navbar_entries': dict}.
    """

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


def notification_count(request):
    """
    Counts the number of notifications the current user has and puts it in
    the 'notification_count' key. If no user, key is unset.

    :param request: The request object.
    :return: The dict {'notification_count': int} | {}
    """

    # Check if logged in
    user = request.user
    if not user.is_authenticated():
        return {}

    return {
        'notification_count': len(user.profile.notifications.filter(read=False))
    }