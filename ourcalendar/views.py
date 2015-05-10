from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def calendar(request):
    return render(request, 'ourcalendar/calendar.jinja', {
        'ext_css': [
            'http://fullcalendar.io/js/fullcalendar-2.3.1/fullcalendar.min.css',
        ],
        'css': [
            'ourcalendar/css/calendar.css',
        ],
        'ext_js': [
            'http://cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js',
            'http://fullcalendar.io/js/fullcalendar-2.3.1/fullcalendar.min.js',
        ],
        'js': [
            'ourcalendar/js/events.js',
        ],
        'js_data': {
            'calendars': [e.serialize() for e in request.user.profile.calendars.get(title='Default').events.all()],
        },
    })

