from django.template.loader import get_template

def send_registration_email(profile):
    # Send the welcome email

    profile.create_html_email(
        subject='Welcome to HitMeUp!',
        body=get_template(
            'communications/emails/registration.jinja'
        ).render({
            'profile': profile,
        })
    ).send(fail_silently=False)
