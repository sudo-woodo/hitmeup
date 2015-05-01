from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'staticpages/home.jinja', {
        'css': [
            'static_pages/css/home.css'
        ],
    })
