from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
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
            'notifications/js/list.jsx',
        ],
        'js_data': {
            'notifications': [
                {
                    'image': 'http://i.ytimg.com/vi/82yHd99YxnY/maxresdefault.jpg',
                    'text': 'FedoraGuy420 has friend requested you!',
                    message: 'Hi I am your bestie yooooooooooo',
                    time: '4 hours ago',
                    read: false,
                    action: '/'
                },
                {
                    image: 'http://i1.kym-cdn.com/entries/icons/facebook/000/011/121/tumblr_m8t7bxSG2k1r61mz1o5_250.gif',
                    text: 'MrSkeltal has friend requested you!',
                    message: 'hey you wanna hang out sometime?',
                    time: '5 hours ago',
                    read: true,
                    action: '/notifications'
                },
                {
                    image: 'https://www.petfinder.com/wp-content/uploads/2012/11/122163343-conditioning-dog-loud-noises-632x475.jpg',
                    text: 'NoNose has friend requested you!',
                    message:'I have no nose so you wanna befriend with me?',
                    time: '3 days ago',
                    read: true,
                    action: '/notifications/1'
                },
                {
                    image: 'http://i0.kym-cdn.com/entries/icons/original/000/013/564/aP2dv.gif',
                    text: 'Wiseman has friend requested you!',
                    message: 'wow zoom how pronounce amaze must fast very space',
                    time: '500 years ago',
                    read: true,
                    action: '/notifications/2'
                }
            ],
        }
    })
