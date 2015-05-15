from django.core.mail import send_mail

def send_test_mail():
    send_mail('Test email', 'The test email worked!', 'aarong4743@optonline.net',
        ['aarong4743@optonline.net'], fail_silently=False)
    print("message sent")
