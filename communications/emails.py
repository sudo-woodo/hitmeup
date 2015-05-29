from django.conf import settings
from django.template.loader import get_template

def render_email(template, context=None):
    # Renders an email template with base variables
    if context is None:
        context = {}

    context.update({
        # Use {{ BASE_URL }}static for static assets in emails
        'BASE_URL': settings.BASE_URL,
    })

    return get_template(template).render(context)

def send_registration_email(profile):
    # Send the welcome email

    profile.create_html_email(
        subject='Welcome to HitMeUp!',
        body=render_email('communications/emails/registration.jinja', {
            'profile': profile,
        })
    ).send(fail_silently=False)
