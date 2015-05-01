from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from user_accounts.forms import UserForm, SignupForm


class SignUpView(View):
    def post(self, request):
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
            return render(request, 'user_accounts/signup.jinja',
                          {'signup_form': signup_form})

    def get(self, request):
        # if the user is already logged in and is trying to access the signup
        # page, return them to home
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Otherwise, return a blank form for the user to fill out
        return render(request, 'user_accounts/signup.jinja', {
            'signup_form': SignupForm()
        })


class LoginView(View):
    def post(self, request):
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
                    return render(request, 'user_accounts/login.jinja', {
                        'login_form': login_form,
                        'error_messages': [
                            'This account has been marked as inactive.'
                        ]
                    })
            # If user provided wrong info, rerender with errors
            else:
                return render(request, 'user_accounts/login.jinja', {
                    'login_form': login_form,
                    'error_messages': [
                        'Incorrect username or password.'
                    ]
                })
        # If there's an form error, rerender with errors
        else:
            return render(request, 'user_accounts/login.jinja', {
                'login_form': login_form
            })

    def get(self, request):
        # if the user is already logged in and is trying to access the login
        # page, return them to home
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Else, display a empty form for the user
        login_form = UserForm()
        return render(request, 'user_accounts/login.jinja', {
            'login_form': login_form
        })


def logout(request):
    return logout_then_login(request)
