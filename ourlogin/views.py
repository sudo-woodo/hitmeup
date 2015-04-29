from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from ourlogin.forms import SignupForm


def signup(request):

    if request.method == 'POST':
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()

            user.set_password(user.password)
            user.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect('/')
        else:
            print signup_form.errors
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            signup_form = SignupForm()

    return render(request, 'ourlogin/oursignup.jinja',
                  {'signup_form': signup_form})


def do_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your HitMeUp account is disabled.")
        else:
            return render(request, 'ourlogin/ourlogin.jinja', {'error': True})

    else:
        return render(request, 'ourlogin/ourlogin.jinja', {})

@login_required
def do_logout(request):
    return logout_then_login(request)
