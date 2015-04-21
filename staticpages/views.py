from django.template.response import TemplateResponse

# Create your views here.
def home(request):
    return TemplateResponse(request, 'staticpages/home.jinja', {
        'css': [
            'staticpages/css/home.css'
        ]
    })
