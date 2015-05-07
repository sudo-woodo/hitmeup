from django.shortcuts import render

# Create your views here.
def list(request):
    return render(request, 'notifications/list.jinja', {
        'css': [
            'notifications/css/list.css'
        ],
        'ext_js': [
            'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.2/'
            'react-with-addons.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.0/'
            'JSXTransformer.js'
        ],
        'jsx': [
            'notifications/jsx/list.jsx'
        ],
    })
