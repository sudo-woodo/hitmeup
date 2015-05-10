from django.shortcuts import render

# Create your views here.
def list(request):
    return render(request, 'notifications/list.jinja', {
        'ext_css': [
            '//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css'
        ],
        'css': [
            'notifications/css/list.css'
        ],
        'ext_js': [
            'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.2/'
            'react-with-addons.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.0/'
            'JSXTransformer.js',
        ],
        'jsx': [
            'notifications/js/list.jsx'
        ],
    })
