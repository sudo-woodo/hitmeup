from haystack.query import SearchQuerySet
from search_bar.forms import UserSearchForm


def do_user_search(data, num_results=None):
    """
    User search logic. Returns a tuple of (username, [suggestions]).
    username can be blank, and suggestions can be empty on error.

    :param data: Form data
    :param num_results: How many results to return; defaults to all
    :return: (string, [string])
    """
    # Ensure we have a query
    query = data['q']
    if not query:
        return (None, [])

    form = UserSearchForm(data=data)
    user = form.search() # form.search() returns a SearchQuerySet

    # Best_match() will get the SearchResult, then you get the user and the username
    username = user.best_match().object.username if user else None

    # The second parameter is the default value. Returns SearchResult object.
    try:
        usernames = SearchQuerySet().autocomplete(user_auto=query)
        first_names = SearchQuerySet().autocomplete(first_name_auto=query)
        last_names = SearchQuerySet().autocomplete(last_name_auto=query)

        # TODO: figure out a logical way to order these in the search results
        # TODO: implement first + last name autocomplete
        suggestions = [result.object.username for result in usernames]
        first_names = [result.object.username for result in first_names]
        last_names = [result.object.username for result in last_names]
        suggestions.extend(first_names)
        suggestions.extend(last_names)

        # Trim the results
        if num_results:
            suggestions = suggestions[:num_results]
    except KeyError:
        suggestions = []

    return (username, suggestions)
