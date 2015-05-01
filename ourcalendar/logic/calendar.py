from ourcalendar.models import Calendar, Event


def get_events(user):
    """Gets all events from a user's calendars."""
    calendars = {}

    for c in Calendar.objects.filter(user=user):
        events = Event.objects.filter(calendar=c).values('id', 'start', 'end', 'title',
                                                         'location', 'description', 'users')
        for e in events:
            e['start'] = e['start'].strftime('%Y-%m-%dT%H:%M:%S')
            e['end'] = e['end'].strftime('%Y-%m-%dT%H:%M:%S')
            e['color'] = c.color
            e['calendar'] = c.title

        calendars[c.title] = list(events)

    return calendars