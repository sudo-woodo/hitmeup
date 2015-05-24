from django.shortcuts import render
from hitmeup import settings

# Create your views here.
def home(request):
    settings.LOGO_URL = request.build_absolute_uri()
    return render(request, 'static_pages/home.jinja', {
        'css': [
            'static_pages/css/home.css'
        ],
    })
