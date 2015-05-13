from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import View



# Filter a search example
"""
class JohnSearchView(SearchView):
    template_name = 'my/special/path/john_search.html'
    queryset = SearchQuerySet().filter(author='john')
    form_class = SearchForm
"""
from django.shortcuts import render_to_response
from .forms import UserSearchForm

class Search(View):
    def post(self, request):
        print request.POST
        form = UserSearchForm(data=request.POST)
        user = form.search() # form.search() returns a SearchQuerySet

        # best_match() will get the SearchResult, then you get the user and the username
        username = user.best_match().object.get_username()
        print username
        return render(request, 'search_bar/usernames.jinja', {'username': username})

def SearchBase(request):
    return render(request, 'search_bar/search.jinja')
