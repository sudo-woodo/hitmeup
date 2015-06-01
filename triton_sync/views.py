from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from triton_sync.forms import TritonLinkLoginForm
from triton_sync.logic.sync import get_classes, AuthenticationException, TritonLinkException, import_schedule


class SyncView(View):
    @method_decorator(login_required)
    def post(self, request):
        login_form = TritonLinkLoginForm(data=request.POST)
        error_message = classes = None

        # Get the user's classes from TritonLink
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            start_date = login_form.cleaned_data['start_date_of_quarter']
            try:
                classes = get_classes(username, password)
            except AuthenticationException:
                error_message = 'Incorrect username or password.'
            except TritonLinkException:
                error_message = 'There was error getting your classes: %s' % TritonLinkException.message
        else:
            return render(request, 'triton_sync/sync.jinja', {
                'login_form': login_form
            })

        if error_message is not None:
            return render(request, 'triton_sync/sync.jinja', {
                'login_form': login_form,
                'error_messages': [error_message]
            })

        # Create events for each of the user's class
        import_schedule(request.user.profile, classes, start_date)
        return redirect(reverse('calendar:view_calendar'))

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'triton_sync/sync.jinja', {
            'login_form': TritonLinkLoginForm()
        })