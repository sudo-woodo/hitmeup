from django.contrib import messages
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
from user_accounts.forms import LoginForm, SignupForm, SignUpExtendedForm, EditProfileForm, \
    EditPasswordForm
from user_accounts.models import Friendship


PROFILE_PIC_SIZE = 125
SETTINGS_TAB = 'settings_tab'
PROFILE_SETTINGS_TAB = 'profile'
PASSWORD_SETTINGS_TAB = 'password'


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
            return render(request, 'user_accounts/signup.jinja', {
                'signup_form': signup_form,
                'css': ['user_accounts/css/signup.css']
            })

    def get(self, request):
        # if the user is already logged in and is trying to access the signup
        # page, return them to home
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Otherwise, return a blank form for the user to fill out
        return render(request, 'user_accounts/signup.jinja', {
            'signup_form': SignupForm(),
            'css': ['user_accounts/css/signup.css']
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
                'css': ['user_accounts/css/signup_extended.css'],
                'signup_extended_form': signup_extended_form
            })

    def get(self, request):
        # If it's not the user's first visit, return them to home
        if request.user.profile.did_extended_signup:
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Otherwise, return a blank form for the user to fill out
        return render(request, 'user_accounts/signup_extended.jinja', {
            'css': ['user_accounts/css/signup_extended.css'],
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
                        'css': ['user_accounts/css/login.css'],
                        'login_form': login_form,
                        'error_messages': [
                            'This account has been marked as inactive.'
                        ]
                    })
            # If user provided wrong info, rerender with errors
            else:
                return render(request, 'user_accounts/login.jinja', {
                    'css': ['user_accounts/css/login.css'],
                    'login_form': login_form,
                    'error_messages': [
                        'Incorrect username or password.'
                    ]
                })
        # If there's an form error, rerender with errors
        else:
            return render(request, 'user_accounts/login.jinja', {
                'css': ['user_accounts/css/login.css'],
                'login_form': login_form
            })

    def get(self, request):
        # if the user is already logged in and is trying to access the login
        # page, return them to home
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('static_pages:home'))

        # Else, display a empty form for the user
        return render(request, 'user_accounts/login.jinja', {
            'css': ['user_accounts/css/login.css'],
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

def render_settings(request, tab='profile', profile_form=None, password_form=None,
                  success_messages=None, error_messages=None):
    profile = request.user.profile

    return render(request, 'user_accounts/edit_settings.jinja', {
        'css': [
            'user_accounts/css/edit_settings.css'
        ],
        'js': [
            'user_accounts/js/edit_settings.js'
        ],
        'tab': tab,
        'profile_pic': profile.get_gravatar_url(PROFILE_PIC_SIZE),
        'profile_form': profile_form or EditProfileForm(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone': profile.phone,
            'bio': profile.bio,
        }),
        'password_form': password_form or EditPasswordForm(),
        'success_messages': success_messages or [],
        'error_messages': error_messages or [],
    })

@login_required
def profile_settings(request):
    profile_form = None
    success_messages = None

    if request.method == 'POST':
        user = request.user
        profile = user.profile
        profile_form = EditProfileForm(data=request.POST)
        success_messages = []

        if profile_form.is_valid():
            for key, val in profile_form.cleaned_data.iteritems():
                if key in {'first_name', 'last_name', 'email'}:
                    setattr(user, key, val.strip())
                else:
                    setattr(profile, key, val.strip())
            user.save()
            profile.save()

            success_messages.append('Successfully updated profile!')

    # Return to form
    return render_settings(request, tab='profile', profile_form=profile_form,
                         success_messages=success_messages)

@login_required
def password_settings(request):
    password_form = None
    error_messages = None
    success_messages = None

    if request.method == 'POST':
        password_form = EditPasswordForm(data=request.POST)
        error_messages = []
        success_messages = []

        if password_form.is_valid():
            current_password = password_form.cleaned_data['current_password']
            new_password = password_form.cleaned_data['new_password']
            confirm_password = password_form.cleaned_data['confirm_password']

            if new_password != confirm_password:
                error_messages.append(
                    'New password and password confirmation don\'t match.'
                )

            # Authenticate the current password
            user = authenticate(username=request.user.username,
                                password=current_password)
            if not user:
                error_messages.append('Incorrect password.')

            # Update the password if no errors
            if not error_messages:
                # Set password
                user.set_password(new_password)
                user.save()
                # Sign user in again
                new_user = authenticate(username=request.user.username,
                                        password=new_password)
                login(request, new_user)
                success_messages.append('Successfully updated password!')

    # Return to form
    return render_settings(request, tab='password', password_form=password_form,
                         error_messages=error_messages,
                         success_messages=success_messages)

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
                'user_accounts/js/profile_calendar_input_form.jsx',
                'user_accounts/js/calendar.jsx',
                'user_accounts/js/profile.jsx',
                'user_accounts/js/event_request_box.jsx',
                'user_accounts/js/options.jsx',
            ],
            'js_data': {

            }
        }

        try:
            profile = User.objects.get(username=username).profile
            context['profile'] = {
                'username': username,
                'gravatar': profile.get_gravatar_url(125),
                'full_name': '***** *********',
                'email': '*******@*****.***',
                'phone': '**********',
                'bio': ''
            }
        except User.DoesNotExist:
            raise Http404("User does not exist")

        if request.user.is_authenticated():
            state = {
                'CLEAN': 0,
                'PENDING': 1,
                'IS_FRIENDS': 2
            }

            # uncensor full_name, bio
            context['profile']['full_name'] = profile.full_name
            context['profile']['bio'] = profile.bio

            context['js_data']['showFriendButton'] = request.user.id != profile.pk
            context['js_data']['profileId'] = profile.pk
            context['friended'] = False
            context['censor'] = False

            # uncensor email, phone if viewing own profile
            if request.user.id == profile.pk:
                context['profile']['email'] = profile.email
                context['profile']['phone'] = profile.phone
                context['profile']['is_free'] = profile.is_free

            try:
                friendship = Friendship.objects.get(
                    from_friend=self.request.user.profile,
                    to_friend=profile
                )
                if friendship.accepted:
                    context['friended'] = True
                    context['js_data']['status'] = state['IS_FRIENDS']

                    # uncensor email, phone
                    context['profile']['email'] = profile.email
                    context['profile']['phone'] = profile.phone
                    context['profile']['is_free'] = profile.is_free
                else:
                    context['js_data']['status'] = state['PENDING']
            except Friendship.DoesNotExist:
                context['js_data']['status'] = state['CLEAN']

        else:
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
            # By default, will grab all events from 1990 -> 2050
            events = request.user.profile.calendars.get(title='Default').get_between()
            flattened_events = []
            for e in events:
                try:
                    flattened_events += e
                except TypeError:
                    flattened_events.append(e)
            user_events = [e.serialize() for e in flattened_events]
            try:
                if is_user:
                    should_display = True
                friend = User.objects.get(username=username).profile
                friendship = request.user.profile.get_friendship(friend)
                if friendship is not None and friendship.accepted:
                    # By default, will grab all events from 1990 -> 2050
                    events = friend.calendars.get(title="Default").get_between()
                    flattened_events = []
                    for e in events:
                        try:
                            flattened_events += e
                        except TypeError:
                            flattened_events.append(e)
                    friend_events = [e.serialize() for e in flattened_events]

                    should_display = True
            except (User.DoesNotExist, Friendship.DoesNotExist):
                pass
        context['js_data']['user_events'] = user_events
        context['js_data']['friend_events'] = friend_events
        context['js_data']['should_display'] = should_display
        context['js_data']['is_user'] = is_user

        return render(request, 'user_accounts/profile.jinja', context)
