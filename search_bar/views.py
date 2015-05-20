from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from .forms import UserSearchForm
import simplejson as json
from haystack.query import SearchQuerySet

class Search(View):
    def get(self, request):
        # Second parameter is the default value.
        sqs = SearchQuerySet().autocomplete(user_auto=request.GET.get('q', "Error: No match"))[:5]
        print sqs
        suggestions = [result.title for result in sqs]
        print "ey"
        # Make sure you return a JSON object, not a bare list.
        # Otherwise, you could be vulnerable to an XSS attack.
        the_data = json.dumps({
            'results': suggestions
        })
        return HttpResponse(the_data, content_type='application/json')
        '''
        form = UserSearchForm(data=request.GET)
        user = form.search() # form.search() returns a SearchQuerySet

        # best_match() will get the SearchResult, then you get the user and the username
        username = user.best_match().object.get_username()
        return HttpResponseRedirect(reverse('user_accounts:user_profile',username=username))
        return render(request, 'search_bar/usernames.jinja', {'username': username})''' # eventually change this to render user profile

    def auto_complete(self, request):
        sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
        suggestions = [result.title for result in sqs]

        print("ey")
        # Make sure you return a JSON object, not a bare list.
        # Otherwise, you could be vulnerable to an XSS attack.
        the_data = json.dumps({
            'results': suggestions
        })
        return HttpResponse(the_data, content_type='application/json')

# probably won't need this in future since search is in navbar
def SearchBase(request):
    return render(request, 'search_bar/search.jinja')
