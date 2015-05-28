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

            # Check if passwords match
            data = signup_form.cleaned_data
            if data['password'] != data['confirm_password']:
                # Return the form with errors
                return render(request, 'user_accounts/signup.jinja', {
                    'signup_form': signup_form,
                    'error_messages': [
                        'Passwords do not match.',
                    ],
                })

            user = signup_form.save()
            user.set_password(user.password)
            user.save()

            # After saving the new user to the db, log them in and redirect
            # to the extended signup page
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('user_accounts:extended_signup'))
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
            profile = user.profile

            profile.did_extended_signup = True
            for key, val in signup_extended_form.cleaned_data.iteritems():
                if val.strip():
                    if key in {'first_name', 'last_name'}:
                        setattr(user, key, val.strip())

                    else:
                        setattr(profile, key, val.strip())

            user.save()
            profile.save()
            return HttpResponseRedirect(reverse('static_pages:home'))

        # If there's an form error, rerender with errors
        else:
            return render(request, 'user_accounts/signup_extended.jinja', {
                'signup_extended_form': signup_extended_form
            })

    def get(self, request):
        # If it's not the user's first visit, return them to home
        if request.user.profile.did_extended_signup:
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Otherwise, return a blank form for the user to fill out
        return render(request, 'user_accounts/signup_extended.jinja', {
            'signup_extended_form': SignUpExtendedForm(),
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
            if updated_fields.viewkeys() & {
                'current_password', 'new_password', 'confirm_password',
            }:
                if 'current_password' not in updated_fields:
                    error_messages.append(
                        'Current password was missing.'
                    )
                    password_valid = False
                if 'new_password' not in updated_fields:
                    error_messages.append(
                        'New password was missing.'
                    )
                    password_valid = False
                if 'confirm_password' not in updated_fields:
                    error_messages.append(
                        'Password confirmation was missing.'
                    )
                    password_valid = False

                # If we're good so far...
                if password_valid:
                    if updated_fields['new_password'] != updated_fields['confirm_password']:
                        error_messages.append(
                            'New password and password confirmation don\'t match.'
                        )
                        password_valid = False

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
                '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/css/'
                'bootstrap-datetimepicker.min.css',
                '//cdnjs.cloudflare.com/ajax/libs/bootstrap-switch/3.3.2/css/bootstrap3/'
                'bootstrap-switch.min.css'
            ],
            'css': [
                'user_accounts/css/profile.css'
            ],
            'ext_js': [
                '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.1/fullcalendar.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react-with-addons.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/react/0.13.0/JSXTransformer.js',
                '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/js/'
                'bootstrap-datetimepicker.min.js',
                '//cdnjs.cloudflare.com/ajax/libs/bootstrap-switch/3.3.2/js/'
                'bootstrap-switch.min.js'
            ],
            'js': [
            ],
            'jsx': [
                'ourcalendar/jsx/datetime_field.jsx',
                'user_accounts/js/input_form.jsx',
                'user_accounts/js/calendar.jsx',
                'user_accounts/js/profile.jsx',
                'user_accounts/js/event_request_box.jsx',
                'user_accounts/js/options.jsx',
            ],
            'js_data': {

            }
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
                context['friended'] = False
                context['censor'] = False

                try:
                    friendship = Friendship.objects.get(
                        from_friend=self.request.user.profile,
                        to_friend=profile
                    )
                    if friendship.accepted:
                        context['friended'] = True
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

        friend_events = []
        user_events = []
        should_display = False
        is_user = username == request.user.username
        if request.user.is_authenticated():
            user_events = [e.serialize() for e in
                                request.user.profile.calendars.get(title='Default').events.all()]
            try:
                if is_user:
                    should_display = True
                friend = User.objects.get(username=username).profile
                friendship = request.user.profile.get_friendship(friend)
                if username != is_user and \
                        friendship is not None and friendship.accepted:
                    friend_events = [e.serialize() for e in
                                     friend.calendars.get(title="Default").events.all()]

                    should_display = True
            except (User.DoesNotExist, Friendship.DoesNotExist):
                pass
        context['js_data']['user_events'] = user_events
        context['js_data']['friend_events'] = friend_events
        context['js_data']['should_display'] = should_display
        context['js_data']['is_user'] = is_user

        return render(request, 'user_accounts/profile.jinja', context)
