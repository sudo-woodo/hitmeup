from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from user_accounts.models import UserProfile


def fb(request):
   # try:
   #      # profile = UserProfile.get(facebook_id=request.GET['487475401404522']) # TODO do this
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
   return render(request, 'fb_login/index.jinja')