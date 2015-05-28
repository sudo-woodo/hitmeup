from django.template.loader import get_template

def send_registration_email(profile):
    # Send the welcome email

    msg = profile.create_email(
        subject='Welcome to HitMeUp!',
        body=get_template(
            'communications/emails/registration.jinja'
        ).render({
            'profile': profile,
        })
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=False)
