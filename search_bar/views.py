from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from search_bar.logic.user_search import do_user_search

def user_search(request):
    user, suggestions = do_user_search(request.GET)

    if user:
        return HttpResponseRedirect(
            reverse('user_accounts:user_profile', args=(user.username,))
        )
    else:
        # TODO: make a nice search results page
        return JsonResponse({'suggestions': [
            s.profile.public_serialized for s in suggestions
        ]})

def user_autocomplete(request):
    user, suggestions = do_user_search(request.GET, 5)

    return JsonResponse({'suggestions': [
        s.profile.public_serialized for s in suggestions
    ]})
