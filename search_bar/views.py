from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from .forms import UserSearchForm
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')

class Search(View):
    def post(self, request):
        print request.POST
        form = UserSearchForm(data=request.POST)
        user = form.search() # form.search() returns a SearchQuerySet

        # best_match() will get the SearchResult, then you get the user and the username
        username = user.best_match().object.get_username()
        '''return HttpResponseRedirect(reverse('user_accounts:user_profile',username=username))'''
        return render(request, 'search_bar/usernames.jinja', {'username': username}) # eventually change this to render user profile

# probably won't need this in future since search is in navbar
def SearchBase(request):
    return render(request, 'search_bar/search.jinja')
