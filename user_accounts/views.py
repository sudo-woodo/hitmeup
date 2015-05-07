from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from user_accounts.forms import SignupForm, UserForm, EditForm, EmailForm, PasswordForm
from django.contrib.auth.models import User


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


class EditView(View):
    def post(self, request):
        if 'save-password' in request.POST:
            password_form = PasswordForm(data=request.POST)
            email_form = EmailForm()
            if password_form.is_valid():
                user = authenticate(username=request.user, password=password_form.cleaned_data['current_password'])
                if user:
                    user.set_password(password_form.cleaned_data['new_password'])
                    user.save()
                    new_user = authenticate(username=request.user, password=request.POST['new_password'])
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('user_accounts:edit'))
                else:
                    return render(request, 'user_accounts/edit.jinja', {
                        'password_form': password_form,
                        'email_form': email_form,
                        'error_messages': [
                            'Incorrect password.'
                        ]
                    })

            else:
                return render(request, 'user_accounts/edit.jinja',{
                    'password_form': password_form, 'email_form': email_form
                })

        if 'save-email' in request.POST:
            password_form = PasswordForm()
            email_form = EmailForm(data=request.POST)
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['email']
                request.user.save()
                return HttpResponseRedirect(reverse('user_accounts:edit'))
            else:
                return render(request, 'user_accounts/edit.jinja',{
                    'password_form': password_form, 'email_form': email_form
                })

    def get(self, request):
        # Only allows user to change account info if logged in
        if request.user.is_authenticated():
            password_form = PasswordForm()
            email_form = EmailForm()
            email_form.__dict__['fields']['email'].widget.attrs['placeholder'] = request.user.email
            return render(request, 'user_accounts/edit.jinja', {
                'password_form': password_form, 'email_form': email_form
            })
        # Else returns to the home page
        return HttpResponseRedirect(reverse('static_pages:home'))

    def list(request):
        return render(request, 'user_accounts/edit.jinja', {
        'ext_js': [
            'http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js'
        ],
    })