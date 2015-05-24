from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import escape
from django.views.generic import View
from user_accounts.forms import LoginForm, SignupForm, SignUpExtendedForm, SettingsForm
from user_accounts.models import Friendship


PROFILE_PIC_SIZE = 125


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
            # if the form is valid, update user and userprofile
            user = request.user
            for key, val in signup_extended_form.cleaned_data.iteritems():
                if val.strip():
                    if key in {'first_name', 'last_name'}:
                        setattr(user, key, val.strip())

                    else:
                        setattr(user.profile, key, val.strip())
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
        login_form = LoginForm(data=request.POST)
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
        return render(request, 'user_accounts/login.jinja', {
            'login_form': LoginForm()
        })


def logout(request):
    return logout_then_login(request)

@login_required
def friends_list(request):
    def serialize(friend):
        friendship = request.user.profile.get_friendship(friend)
        serialized = friend.basic_serialized
        serialized['favorite'] = friendship.favorite
        return serialized

    return render(request, 'user_accounts/friends_list.jinja', {
        'css': [
            'user_accounts/css/friends_list.css'
        ],
        'ext_js': [
            '//cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react-with-addons.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/react/0.13.0/JSXTransformer.js',
        ],
        'jsx': [
            'user_accounts/js/friends_list.jsx',
        ],
        'js_data': {
            'friends': [serialize(f) for f in
                        request.user.profile.friends]
        },
    })


class SettingsView(View):
    def post(self, request):
        profile = request.user.profile
        edit_form = SettingsForm(data=request.POST)
        error_messages = []
        success_messages = []

        # To see if we need to update password
        update_password = False
        password_valid = True

        if edit_form.is_valid():
            # Get non-empty field values
            updated_fields = {k: v for k, v
                              in edit_form.cleaned_data.iteritems() if v}

            # Manually check password fields
            if updated_fields.viewkeys() & {'current_password', 'new_password'}:
                if 'current_password' not in updated_fields:
                    error_messages.append(
                        'New password given, but current password was missing.'
                    )
                    password_valid = False
                elif 'new_password' not in updated_fields:
                    error_messages.append(
                        'Current password given, but new password was missing.'
                    )
                    password_valid = False
                else:
                    # Authenticate the current password
                    user = authenticate(username=request.user.username,
                                        password=updated_fields['current_password'])
                    if user:
                        update_password = True
                    else:
                        error_messages.append('Incorrect password.')
                        password_valid = False

            # Only proceed if password valid
            if password_valid:
                # Update password
                if update_password:
                    # Set password
                    request.user.set_password(updated_fields['new_password'])
                    request.user.save()
                    profile.save()
                    # Sign user in again
                    new_user = authenticate(username=request.user.username,
                                            password=updated_fields['new_password'])
                    login(request, new_user)

                # Update other fields
                if not error_messages:
                    for key, val in updated_fields.iteritems():
                        if key in {'first_name', 'last_name', 'email'}:
                            setattr(request.user, key, val.strip())
                        else:
                            setattr(profile, key, val.strip())
                    request.user.save()
                    profile.save()

                success_messages.append('Successfully updated!')

        # Return to form
        return render(request, 'user_accounts/edit_settings.jinja', {
            'css': [
                'user_accounts/css/edit_settings.css'
            ],
            'profile_pic': profile.get_gravatar_url(PROFILE_PIC_SIZE),
            'edit_form': edit_form,
            'error_messages': error_messages,
            'success_messages': success_messages,
        })

    def get(self, request):
        profile = request.user.profile
        return render(request, 'user_accounts/edit_settings.jinja', {
            'css': [
                'user_accounts/css/edit_settings.css'
            ],
            'profile_pic': profile.get_gravatar_url(PROFILE_PIC_SIZE),
            'edit_form': SettingsForm(initial={
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,
                'phone': profile.phone,
                'bio': profile.bio
            })
        })


class UserProfile(View):
    def get(self, request, username):
        context = {
            'ext_css': [
                '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.1/fullcalendar.min.css',
            ],
            'css': [
                'user_accounts/css/profile.css'
            ],
            'ext_js': [
                '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.1/fullcalendar.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react-with-addons.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/react/0.13.0/JSXTransformer.js',
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
