from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'staticpages/index.html', {
        'css': [
            'staticpages/css/index.css'
        ]
    })
