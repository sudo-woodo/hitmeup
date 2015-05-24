from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from hitmeup import settings

#our initial test mail sending function
def send_test_mail():
#    send_mail('Test email', 'The test email worked!', 'sudowoodohitmeup@gmail.com',
 #       ['sudowoodohitmeup@gmail.com'], fail_silently=False)
  #  print("message sent")
    #create new EmailMessage object sending a message from sudowoodo email to sudowoodoemail
    email = EmailMessage('Hello', 'Body goes here', 'sudowoodohitmeup@gmail.com',
            ['sudowoodohitmeup@gmail.com', 'to2@example.com'], ['bcc@example.com'],
            reply_to=['another@example.com'], headers={'Message-ID': 'foo'})
    #send the email
    email.send(fail_silently=False)
    print("message sent")

def send_welcome_email(profile):
    #send the welcome email
    print "URL is: " + settings.LOGO_URL
    #creare the email based on the user
    msg = profile.create_email(
        #set the welcome subject
        subject='Welcome to HitMeUp!',
        #use welcome.jinja as body of email
        body=get_template(
            'communications/emails/welcome.jinja'
        ).render({'profile': profile, 'absolute_logo_uri' : settings.LOGO_URL})
    )
    #tell Django that content of welcome.jinja is html
    msg.content_subtype = "html"
    #send the message
    msg.send(fail_silently=False)
    print("signup message sent")
#def send_registration_email(user):
 #   subject = "wooo"
  #  body = "welcome, %s" % user.username
   # sender = "welcome@sudowoodo.com"
    #recipient = user.email

    #send_mail(subject, body, sender, recipient, fail_silently=False)