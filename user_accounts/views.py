from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import escape
from django.views.generic import View
from user_accounts.forms import UserForm, SignupForm, SignUpExtendedForm, EditForm
from user_accounts.models import Friendship


class SignUpView(View):
    def post(self, request):
        # Fill out form with request data
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.set_password(user.password)
            user.save()

            # After saving the new user to the db, log them in and redirect
            # to the extended signup page
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('user_accounts:extended_signup')
                                        + '?first_visit=true')
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


class SignUpExtended(View):
    def post(self, request):
        # Fill out form with request data
        signup_extended_form = SignUpExtendedForm(data=request.POST)
        if signup_extended_form.is_valid():
            # if the form is valid, update userprofile model
            user = request.user
            updatedFields = []
            for key, val in signup_extended_form.cleaned_data.iteritems():
                if val != u'':
                    if key == 'first_name' or key == 'last_name':
                        updatedFields.append(key)
                        setattr(
                            user,
                            key,
                            val
                        )

                    else:
                        updatedFields.append(key)
                        setattr(
                            user.profile,
                            key,
                            val
                        )
            user.save()
            user.profile.save()
            return HttpResponseRedirect(reverse('static_pages:home'))
        # If there's an form error, rerender with errors
        else:
            return render(request, 'user_accounts/signup_extended.jinja', {
                'signup_extended_form': signup_extended_form
            })

    def get(self, request):
        # If it's not the user's first visit, return them to home
        if not request.GET.get('first_visit', False) == 'true':
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Otherwise, return a blank form for the user to fill out
        return render(request, 'user_accounts/signup_extended.jinja', {
            'signup_extended_form': SignUpExtendedForm()
        })


class LoginView(View):
    def post(self, request):
        # Fill out form with request data
        login_form = UserForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])
            if user:
                # If the user is active, log them in and redirect to next
                # destination if specified; if not, redirect to home
                if user.is_active:
                    login(request, user)
                    destination = request.GET.get(
                        'next',
                        reverse('static_pages:home')
                    )
                    return HttpResponseRedirect(escape(destination))

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


class EditAccountView(View):
    def post(self, request):
        # Profile of user logged in
        profile = request.user.profile
        # Creates form with initial values
        edit_form = EditForm(data=request.POST)
        if edit_form.is_valid():
            # Iterator to iterate form
            updated_fields = {}
            # Gets non-empty field values
            for key, val in edit_form.cleaned_data.iteritems():
                if val != u'':
                    updated_fields[key] = val

            # Password is not empty
            if updated_fields.viewkeys() >= {'current_password', 'new_password'}:
                # Authenticates the "current password"
                user = authenticate(username=request.user.username,
                                    password=updated_fields['current_password'])
                if user:
                    # Update new field values
                    for key in updated_fields:
                        if key == 'first_name' or key == 'last_name' or key == 'email':
                            setattr(
                                request.user,
                                key,
                                updated_fields[key]
                            )
                        else:
                            setattr(
                                profile,
                                key,
                                updated_fields[key]
                            )
                    # Sets password
                    request.user.set_password(updated_fields['new_password'])
                    request.user.save()
                    profile.save()
                    # Signs user in again
                    new_user = authenticate(username=request.user.username,
                                            password=updated_fields['new_password'])
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('user_accounts:edit_account'))
                else:
                    return render(request, 'user_accounts/edit.jinja',
                                  {'edit_form': EditForm(initial={'first_name': profile.first_name,
                                                                  'last_name': profile.last_name,
                                                                  'email': profile.email,
                                                                  'phone': profile.phone,
                                                                  'bio': profile.bio}),
                                   'error_messages': ['Incorrect password.']
                                   })
            # 1 missing password field
            elif updated_fields.viewkeys() >= {'current_password'} or updated_fields.viewkeys() >= {'new_password'}:
                # Sets error message
                if 'current_password' not in updated_fields:
                    error = ['Must enter current password.']
                else:
                    error = ['Must enter new password.']
                return render(request, 'user_accounts/edit.jinja',
                              {'edit_form': EditForm(initial={'first_name': profile.first_name,
                                                              'last_name': profile.last_name,
                                                              'email': profile.email,
                                                              'phone': profile.phone,
                                                              'bio': profile.bio}),
                               'error_messages': error
                               })
            # Assumes user does not want to change password
            else:
                # Iterates through dictionary
                for key in updated_fields:
                        if key == 'first_name' or key == 'last_name' or key == 'email':
                            setattr(
                                request.user,
                                key,
                                updated_fields[key]
                            )
                        else:
                            setattr(
                                profile,
                                key,
                                updated_fields[key]
                            )
                request.user.save()
                profile.save()
                return HttpResponseRedirect(reverse('user_accounts:edit_account'))
        else:
            # Sets both initial and placeholder value
            return render(request, 'user_accounts/edit.jinja',{
                'edit_form': edit_form
            })

    def get(self, request):
        # Only allows user to change account info if logged in
        profile = request.user.profile
        if request.user.is_authenticated():
            return render(request, 'user_accounts/edit.jinja',
                          {'edit_form': EditForm(initial={'first_name': profile.first_name,
                                                          'last_name': profile.last_name,
                                                          'email': profile.email,
                                                          'phone': profile.phone,
                                                          'bio': profile.bio}),
                           })
        # Else returns to the home page
        return HttpResponseRedirect(reverse('static_pages:home'))


class UserProfile(View):
    def get(self, request, username):
        context = {
            'ext_css': [
                'http://fullcalendar.io/js/fullcalendar-2.3.1/'
                'fullcalendar.min.css'
            ],
            'css': [
                'user_accounts/css/profile.css'
            ],
            'ext_js': [
                'http://cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/'
                'moment.min.js',
                'http://fullcalendar.io/js/fullcalendar-2.3.1/'
                'fullcalendar.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.2/'
                'react-with-addons.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.0/'
                'JSXTransformer.js',
            ],
            'js': [
                'user_accounts/js/testcalendar.js'
            ],
            'jsx': [
                'user_accounts/js/profile.jsx'
            ],
            'js_data': {}
        }

        if request.user.is_authenticated():
            state = {
                'CLEAN': 0,
                'PENDING': 1,
                'IS_FRIENDS': 2
            }

            try:
                profile = User.objects.get(username=username).profile
                context['profile'] = profile
                context['js_data']['showFriendButton'] = request.user.id != profile.pk
                context['js_data']['profileId'] = profile.pk
                context['censor'] = False

                try:
                    friendship = Friendship.objects.get(
                        from_friend=self.request.user.profile,
                        to_friend=profile
                    )
                    if friendship.accepted:
                        context['js_data']['status'] = state['IS_FRIENDS']
                    else:
                        context['js_data']['status'] = state['PENDING']
                except Friendship.DoesNotExist:
                    context['js_data']['status'] = state['CLEAN']

            except User.DoesNotExist:
                raise Http404("User does not exist")
        else:
            context['profile'] = {
                'username': username,
                'full_name': '***** *********',
                'email': '*******@*****.***',
                'phone': '**********',
                'bio': ''
            }

            return_url = reverse('user_accounts:login')
            return_url += '?next='
            return_url += reverse(
                'user_accounts:user_profile',
                args={username}
            )

            context['return_url'] = return_url
            context['js_data']['showFriendButton'] = False
            context['censor'] = True

        return render(request, 'user_accounts/profile.jinja', context)
