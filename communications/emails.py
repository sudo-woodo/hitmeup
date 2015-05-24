from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from hitmeup import settings


def send_test_mail():
#    send_mail('Test email', 'The test email worked!', 'sudowoodohitmeup@gmail.com',
 #       ['sudowoodohitmeup@gmail.com'], fail_silently=False)
  #  print("message sent")

    email = EmailMessage('Hello', 'Body goes here', 'sudowoodohitmeup@gmail.com',
            ['sudowoodohitmeup@gmail.com', 'to2@example.com'], ['bcc@example.com'],
            reply_to=['another@example.com'], headers={'Message-ID': 'foo'})

    email.send(fail_silently=False)
    print("message sent")

def send_welcome_email(profile):
    print "URL is: " + settings.LOGO_URL
    msg = profile.create_email(
        subject='Welcome to HitMeUp!',
        body=get_template(
            'communications/emails/welcome.jinja'
        ).render({'profile': profile, 'absolute_logo_uri' : settings.LOGO_URL})
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=False)
    print("signup message sent")
#def send_registration_email(user):
 #   subject = "wooo"
  #  body = "welcome, %s" % user.username
   # sender = "welcome@sudowoodo.com"
    #recipient = user.email

    #send_mail(subject, body, sender, recipient, fail_silently=False)