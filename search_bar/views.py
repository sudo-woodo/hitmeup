from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.views.generic import View
from haystack.query import SearchQuerySet
import json
from .forms import UserSearchForm


NUM_AUTOCOMPLETE = 5


class UserSearch(View):

    @staticmethod
    def do_search(data):
        """
        User search logic. Returns a tuple of (username, [suggestions]).
        username can be blank, and suggestions can be empty on error.

        :param data: Form data
        :return: (string, [string])
        """
        form = UserSearchForm(data=data)
        user = form.search() # form.search() returns a SearchQuerySet

        # Best_match() will get the SearchResult, then you get the user and the username
        username = user.best_match().object.get_username() if user else None

        # The second parameter is the default value. Returns SearchResult object.
        try:
            sqs = SearchQuerySet().autocomplete(
                user_auto=data['q'])[:NUM_AUTOCOMPLETE]
            suggestions = [result.object.get_username() for result in sqs]
        except KeyError:
            suggestions = []

        return (username, suggestions)

    # For page view
    def get(self, request):
        username, suggestions = self.do_search(request.GET)

        if username:
            return HttpResponseRedirect(
                reverse('user_accounts:user_profile', args=(username,))
            )
        else:
            # TODO: make a nice search results page
            return JsonResponse({'suggestions': suggestions})

    # For autocomplete box
    def post(self, request):
        username, suggestions = self.do_search(request.POST)

        return JsonResponse({'suggestions': suggestions})
