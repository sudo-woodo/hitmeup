from django.shortcuts import render
from hitmeup import settings

# Create your views here.
def home(request):
    #Create an abolute URL for the HitMeUp logo image and save it in settings for later use
    settings.LOGO_URL = request.build_absolute_uri()
    return render(request, 'static_pages/home.jinja', {
        'css': [
            'static_pages/css/home.css'
        ],
    })
