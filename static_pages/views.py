from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'static_pages/home.jinja', {
        'css': [
            'static_pages/css/home.css'
        ],
    })
