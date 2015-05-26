from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from search_bar.logic.user_search import do_user_search

def user_search(request):
    username, suggestions = do_user_search(request.GET)

    if username:
        return HttpResponseRedirect(
            reverse('user_accounts:user_profile', args=(username,))
        )
    else:
        # TODO: make a nice search results page
        return JsonResponse({'suggestions': suggestions})

def user_autocomplete(request):
    username, suggestions = do_user_search(request.GET, 5)

    return JsonResponse({'suggestions': suggestions})
