from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'staticpages/home.jinja', {
        'css': [
            'staticpages/css/home.css'
        ]
    })
