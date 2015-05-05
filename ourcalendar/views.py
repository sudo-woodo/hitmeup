from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ourcalendar.logic.calendar import get_events

@login_required
def calendar(request):
    return render(request, 'ourcalendar/calendar.jinja', {
        'ext_css': [
            'http://fullcalendar.io/js/fullcalendar-2.3.1/fullcalendar.min.css',
        ],
        'css': [
            'ourcalendar/css/calendar.css',
            'ourcalendar/css/bootstrap-datetimepicker.css',
        ],
        'ext_js': [
            'http://cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js',
            'http://fullcalendar.io/js/fullcalendar-2.3.1/fullcalendar.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react-with-addons.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.0/JSXTransformer.js',
        ],
        'js': [
            'vendor/js/bootstrap-datetimepicker.min.js',
            'ourcalendar/js/events.js',

        ],
        'jsx': [
            'ourcalendar/jsx/datetimefield.jsx',
            'ourcalendar/jsx/eventmodal.jsx'
        ],
        'js_data': {
            'calendars': get_events(request.user),
        },
    })