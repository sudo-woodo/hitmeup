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
