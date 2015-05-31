from django.contrib.auth import *
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from user_accounts.models import UserProfile
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User


def fb(request):
    # try:
    # # profile = UserProfile.get(facebook_id=request.GET['487475401404522']) # TODO do this
    #      profile = UserProfile.objects.all().get(facebook_id='487475401404522')
    #      # print "success!"
    # except KeyError:
    #      return # handle case of no id
    # except UserProfile.DoesNotExist:
    #      return # redirect to signup with ?facebook_id=whatever
    #
    # # if we got here, means we have an existing user, sign them in
    # new_user = profile.user
    #
    # login(request, new_user)
    # return HttpResponseRedirect(reverse('user_accounts:extended_signup')
    #                              + '?first_visit=true')

    context = RequestContext(request,
                             {'request': request,
                              'user': request.user,
                              'anonymous': request.user.is_anonymous()})
    # print context
    # # print not request.user.is_anonymous()
    # if not request.user.is_anonymous():
    #     if User.objects.filter(email=request.user.email).count():
    #         print "check if the user has verified HitMeUp account"
    #         if not User.objects.filter(email=request.user.email)[0].profile.verified:
    #             # if the user hasn't verified
    #             print "not verified. redirect the user to a verifying page"
    #         else:
    #             print "sign this user in"
    # else:  # the user's email is not in our database
    #     print "redirect the user to a new sign-up page"


    return render_to_response('fb_login/home.html',
                          context_instance=context)