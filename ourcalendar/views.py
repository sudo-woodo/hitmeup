from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def calendar(request):
    return render(request, 'ourcalendar/calendar.jinja', {
        'ext_css': [
            '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.1/fullcalendar.min.css',
            '//cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css',
            '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.1/fullcalendar.min.css',
            '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/css/'
            'bootstrap-datetimepicker.min.css',
        ],
        'css': [
            'ourcalendar/css/calendar.css',
        ],
        'ext_js': [
            '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.1/fullcalendar.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react-with-addons.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/react/0.13.0/JSXTransformer.js',
            '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/js/'
            'bootstrap-datetimepicker.min.js',
        ],
        'js': [
            'ourcalendar/js/events.js',
        ],
        'jsx': [
            'ourcalendar/jsx/event_modal_error.jsx',
            'ourcalendar/jsx/datetime_field.jsx',
            'ourcalendar/jsx/input_form.jsx',
            'ourcalendar/jsx/create_event_modal.jsx',
            'ourcalendar/jsx/event_detail_modal.jsx'
        ],
    })

