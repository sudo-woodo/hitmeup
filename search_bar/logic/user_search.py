from haystack.query import SearchQuerySet
from search_bar.forms import UserSearchForm


NUM_AUTOCOMPLETE = 5


def do_user_search(data):
    """
    User search logic. Returns a tuple of (username, [suggestions]).
    username can be blank, and suggestions can be empty on error.

    :param data: Form data
    :return: (string, [string])
    """
    form = UserSearchForm(data=data)
    user = form.search() # form.search() returns a SearchQuerySet

    # Best_match() will get the SearchResult, then you get the user and the username
    username = user.best_match().object.username if user else None

    # The second parameter is the default value. Returns SearchResult object.
    try:
        sqs = SearchQuerySet().autocomplete(
            user_auto=data['q'])[:NUM_AUTOCOMPLETE]
        suggestions = [result.object.username for result in sqs]
    except KeyError:
        suggestions = []

    return (username, suggestions)
