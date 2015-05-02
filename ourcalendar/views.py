from django.shortcuts import render
from .models import Event, Calendar
from ourcalendar.forms import EventForm

def calendar(request):
    calendars = {}

    for c in Calendar.objects.all():
        events = Event.objects.filter(calendar=c).values('start', 'end', 'title', 'location', 'description', 'users')
        for e in events:
            e['start'] = e['start'].strftime('%Y-%m-%dT%H:%M:%S')
            e['end'] = e['end'].strftime('%Y-%m-%dT%H:%M:%S')
            e['color'] = c.color
            e['calendar'] = c.title
        calendars[c.title] = list(events)

    context = {
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
            'calendars': calendars,
        },
    }
    return render(request, 'ourcalendar/calendar.jinja', context)

