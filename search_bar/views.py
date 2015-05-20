from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from .forms import UserSearchForm
import simplejson as json
from haystack.query import SearchQuerySet

class Search(View):
    def get(self, request):
        form = UserSearchForm(data=request.GET)
        user = form.search() # form.search() returns a SearchQuerySet
        if user:
            # Best_match() will get the SearchResult, then you get the user and the username
            username = user.best_match().object.get_username()
            # return HttpResponseRedirect(reverse('user_accounts:user_profile',username=username))
            return render(request, 'search_bar/usernames.jinja', {'username': username}) # eventually change this to render user profile

        # Not an exact username, need auto-complete!
        else:
            # The second parameter is the default value. Returns SearchResult object.
            sqs = SearchQuerySet().autocomplete(user_auto=request.GET.get('q', "Error: No match"))[:5]
            suggestions = [result.object.get_username() for result in sqs]

            # Make sure you return a JSON object, not a bare list,
            # otherwise you could be vulnerable to an XSS attack.
            the_data = json.dumps({
                'results': suggestions
            })
            return HttpResponse(the_data, content_type='application/json') # change this later

# Probably won't need this in future since search is in navbar
def SearchBase(request):
    return render(request, 'search_bar/search.jinja')
