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
        print "sup"
        print request.POST
        form = UserSearchForm(data=request.POST)
        print form
        username = form.search()
        print username
        return render_to_response('search_bar/usernames.jinja', {'username': username})

def SearchBase(request):
    print "looka da flick a da wrist"
    #results = search #nonworking example
    #return render(request, 'search_bar/search.jinja', {'search': results})
    return render(request, 'search_bar/search.jinja')
