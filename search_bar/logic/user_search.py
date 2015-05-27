from haystack.query import SearchQuerySet
from search_bar.forms import UserSearchForm


def do_user_search(data, num_results=None):
    """
    User search logic. Returns a tuple of (User, [User suggestions]).
    User can be None, and suggestions can be empty on error.

    :param data: Form data
    :param num_results: How many results to return; defaults to all
    :return: (User, [User])
    """
    # Ensure we have a query
    query = data['q']
    if not query:
        return (None, [])

    form = UserSearchForm(data=data)
    search_results = form.search() # form.search() returns a SearchQuerySet

    # Best_match() will get the SearchResult, then you get the user and the username
    user = search_results.best_match().object if search_results else None

    # The second parameter is the default value. Returns SearchResult object.
    try:
        auto_results = SearchQuerySet()\
            .filter_or(username_auto=query)\
            .filter_or(first_name_auto=query)\
            .filter_or(last_name_auto=query)

        suggestions = [result.object for result in auto_results]

        # Trim the results
        if num_results:
            suggestions = suggestions[:num_results]
    except KeyError:
        suggestions = []

    return (user, suggestions)
