from django.shortcuts import render, redirect

# Create your views here.
from communications.emails import send_test_mail

def email_test(request):
    print('reached email_test view')
    send_test_mail()
    return redirect('static_pages:home')
    # return render(request, 'communications/emails/welcome.jinja')