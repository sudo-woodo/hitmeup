from django.conf import settings
from django.template.loader import get_template

def render_email(template, profile, context=None):
    # Renders an email template with base variables
    if context is None:
        context = {}

    context.update({
        # Use {{ BASE_URL }}static for static assets in emails
        'BASE_URL': settings.BASE_URL,
        'profile': profile,
    })

    return get_template(template).render(context)

def send_registration_email(profile):
    # Send the welcome email

    profile.create_html_email(
        subject='Welcome to HitMeUp!',
        body=render_email('communications/emails/registration.jinja', profile)
    ).send(fail_silently=False)

def send_notification_email(notification):
    # Send the notification email

    notification.recipient.create_html_email(
        subject='A Notification from HitMeUp',
        body=render_email('communications/emails/notification.jinja', notification.recipient, {
            'notification': notification,
        })
    ).send(fail_silently=False)
