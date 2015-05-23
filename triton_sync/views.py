from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from triton_sync.forms import TritonLinkLoginForm
from triton_sync.logic.sync import get_classes, AuthenticationException, TritonLinkException, import_schedule


class LoginView(View):
    @method_decorator(login_required)
    def post(self, request):
        login_form = TritonLinkLoginForm(data=request.POST)
        classes = []

        # Get the user's classes from TritonLink
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                classes = get_classes(username, password)
            except AuthenticationException:
                return render(request, 'triton_sync/sync.jinja', {
                    'login_form': login_form,
                    'error_messages': [
                        'Incorrect username or password.'
                    ]
                })
            except TritonLinkException:
                return render(request, 'triton_sync/sync.jinja', {
                    'login_form': login_form,
                    'error_messages': [
                        'There was error getting your classes: %s' % TritonLinkException.message
                    ]
                })

        # Create events for each of the user's class
        import_schedule(request.user.profile, classes)
        return redirect(reverse('calendar:view_calendar'))

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'triton_sync/sync.jinja', {
            'login_form': TritonLinkLoginForm()
        })