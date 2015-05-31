from django.contrib.auth.models import User
from haystack.query import SearchQuerySet


MAX_QUERY_LENGTH = 100


def do_user_search(data, num_results=None):
    """
    User search logic. Returns a tuple of (User, [User suggestions]).
    User can be None, and suggestions can be empty on error.

    :param data: Form data
    :param num_results: How many results to return; defaults to all
    :return: (User, [User])
    """
    # Ensure we have a query and it's not too long
    query = data.get('q')
    if (not query) or len(query) > MAX_QUERY_LENGTH:
        return (None, [])

    # Try for an exact match
    try:
        user = User.objects.get(username=query)
    except User.DoesNotExist:
        user = None

    # Returns SearchResult object.
    try:
        auto_results = SearchQuerySet()\
            .filter_or(username_auto=query)\
            .filter_or(first_name_auto=query)\
            .filter_or(last_name_auto=query)\
            .filter_or(full_name_auto=query)

        suggestions = [result.object for result in auto_results]

        # Trim the results
        if num_results:
            suggestions = suggestions[:num_results]
    except KeyError:
        suggestions = []

    return (user, suggestions)
