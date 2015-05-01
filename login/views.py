from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from login.forms import UserForm, SignupForm


def do_signup(request):
    if request.method == 'POST':

        # Fill out form with request data
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.set_password(user.password)
            user.save()

            # After saving the new user to the db, log them in and redirect
            # to home page
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('static_pages:home'))
        else:

            # Return the form with errors
            return render(request, 'login/signup.jinja',
                          {'signup_form': signup_form})

    # if the user is already logged in and is trying to access the signup
    # page, return them to home
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('static_pages:home'))

    # if it is not a POST request, just return a blank form for the user
    # to fill out
    return render(request, 'login/signup.jinja',
                  {'signup_form': SignupForm()})


def do_login(request):
    if request.method == 'POST':
        # Fill out form with request data
        login_form = UserForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])

            if user:
                # if the user is active, log them in and redirect to home
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('static_pages:home'))
                else:
                    return render(request, 'login/login.jinja', {
                        'login_form': login_form,
                        'error_messages': [
                            'This account has been marked as inactive.'
                        ]
                    })

            # If user provided wrong info, rerender with errors
            else:
                return render(request, 'login/login.jinja', {
                    'login_form': login_form,
                    'error_messages': [
                        'Incorrect username or password.'
                    ]
                })
        # If there's an form error, rerender with errors
        else:
            return render(request, 'login/login.jinja', {
                'login_form': login_form
            })

    else:
        # if the user is already logged in and is trying to access the login
        # page, return them to home
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('static_pages:home'))

        login_form = UserForm()
        return render(request, 'login/login.jinja', {'login_form': login_form})


@login_required
def do_logout(request):
    return logout_then_login(request)
