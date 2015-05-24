from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render
from notifications.models import Notification


@login_required
def list(request):
    notifications = request.user.profile.notifications.all()

    # Mark all notifications as read, but revert (not save) for display
    for n in notifications:
        if not n.read:
            n.read = True
            n.save()
            n.read = False

    return render(request, 'notifications/list.jinja', {
        'css': [
            'notifications/css/list.css'
        ],
        'ext_js': [
            '//cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react-with-addons.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/react/0.13.0/JSXTransformer.js',
        ],
        'jsx': [
            'notifications/js/list.jsx',
        ],
        'js_data': {
            'notifications': [n.serialized for n in notifications]
        }
    })

# Marks a notification as read and redirects to the 'next'.
# One day, when we implement pop-up notification hub...
# TODO TEST ME WHEN WE ACTUALLY USE THIS
@login_required
def action(request, notification_id):
    # Marks a notification as read, and redirects to "next" querystring param
    try:
        notification = request.user.profile.notifications.get(id=notification_id)
        notification.read = True
        notification.save()
    except Notification.DoesNotExist:
        raise Http404("Notification to mark read not found")

    return HttpResponseRedirect(
        request.GET.get('next', reverse('static_pages:home'))
    )
