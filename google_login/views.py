from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'google_login/login.jinja', {
        'ext_js': [
            'https://apis.google.com/js/platform.js'
        ]
    })