from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from search_bar.logic.user_search import do_user_search
from user_accounts.models import Friendship


def user_search(request):
    query = request.GET.get('q')

    # Easter egg time!
    if query == 'hestia!':
        return HttpResponseRedirect('http://hestia.dance/')
    elif query == 'yousmell!':
        return HttpResponseRedirect('https://scontent-sjc2-1.xx.fbcdn.net/'
                                    'hphotos-ash2/t31.0-8/'
                                    '338205_203999436341625_1022386334_o.jpg')

    user, suggestions = do_user_search(request.GET)

    if user:
        return HttpResponseRedirect(
            reverse('user_accounts:user_profile', args=(user.username,))
        )
    else:
        friends = []
        others = []

        for suggestion in suggestions:
            profile = suggestion.profile
            try:
                request.user.profile.get_friendship(profile)
                friends.append((profile, True))
            except Friendship.DoesNotExist:
                others.append((profile, False))

        return render(request, 'search_bar/result.jinja', {
            'css': [
                'search_bar/css/result.css',
                'user_accounts/css/friends_list.css',
            ],
            'results': friends + others,

        })

def user_autocomplete(request):
    user, suggestions = do_user_search(request.GET, 5)

    return JsonResponse({'suggestions': [
        s.profile.public_serialized for s in suggestions
    ]})
