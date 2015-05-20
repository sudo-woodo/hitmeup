
$(document).ready(function() {
    var cal = $('#calendar');
    var events = $HMU.user_events;
    var friend_events = $HMU.friend_events;

    friend_events = friend_events.map(function(event) {
        event.rendering = "inverse-background";
        event.id = 1;
        event.color = '#257e4a';
        event.title = "Busy";
        return event;
    });

    $.merge(events, friend_events);

    cal.fullCalendar({
        events: events,
        defaultView: "agendaWeek",
        allDaySlot: false,
        scrollTime: "08:00:00",

        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        }
    });



});
//TODO Actually link this up to user's calendar and add censoring