from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from login.forms import SignupForm


def signup(request):
    if request.method == 'POST':

        # Fill out form with request data
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()

            user.set_password(user.password)
            user.save()

            # After saving the new user to the db, log them in and redirect to home page
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect('/')
        else:

            # if the username requested already exists, rerender the view with an empty form and warning alert
            if User.objects.filter(username=request.POST['username']).exists():
                return render(request, 'login/signup.jinja',
                              {'signup_form': signup_form, 'error': True})
    else:

        # if the user is already logged in and is trying to access the signup page, return them to home
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        # if it is not a POST request, just return a blank form for the user to fill out
        else:
            signup_form = SignupForm()

    return render(request, 'login/signup.jinja',
                  {'signup_form': signup_form})


def do_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:

            # if the user is active, log them in and redirect to home
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your HitMeUp account is disabled.")

            # if the user doesn't exist, refresh the page with a blank form and an error alert
        else:
            return render(request, 'login/login.jinja', {'error': True})

    else:
        return render(request, 'login/login.jinja', {})


@login_required
def do_logout(request):
    return logout_then_login(request)
