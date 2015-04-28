from django.shortcuts import render
from django.core import serializers
from .models import Event


def calendar(request):
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
            'events': serializers.serialize('json', Event.objects.all()),
        },
    }
    return render(request, 'ourcalendar/calendar.jinja', context)