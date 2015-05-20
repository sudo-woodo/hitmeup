from django.core.mail import send_mail
from django.core.mail import EmailMessage

def send_test_mail():
#    send_mail('Test email', 'The test email worked!', 'sudowoodohitmeup@gmail.com',
 #       ['sudowoodohitmeup@gmail.com'], fail_silently=False)
  #  print("message sent")

    email = EmailMessage('Hello', 'Body goes here', 'sudowoodohitmeup@gmail.com',
            ['sudowoodohitmeup@gmail.com', 'to2@example.com'], ['bcc@example.com'],
            reply_to=['another@example.com'], headers={'Message-ID': 'foo'})

    email.send(fail_silently=False)
    print("message sent")
#def send_registration_email(user):
 #   subject = "wooo"
  #  body = "welcome, %s" % user.username
   # sender = "welcome@sudowoodo.com"
    #recipient = user.email

    #send_mail(subject, body, sender, recipient, fail_silently=False)