from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'static_pages/home.jinja', {
        'ext_css': [
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/'
            'font-awesome.min.css',
        ],
        'css': [
            'static_pages/css/home.css'
        ],
    })
