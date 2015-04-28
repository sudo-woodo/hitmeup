var events = $.map(JSON.parse($HMU.events), function(e) {
    var event = e.fields;
    return {
        title: event.title,
        start: moment(event.start).format("YYYY-MM-DDTHH:mm:ss"),
        end: moment(event.end).add(1, 'hour').format("YYYY-MM-DDTHH:mm:ss")
    }
});

var prevClick;
$(document).ready(function() {
    $('#calendar').fullCalendar({
        editable: true,
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        dayClick: function() {
            if (prevClick)
                $(prevClick).css('background-color', 'white');
            $(this).css('background-color', 'rgba(204,255,249,0.3)');
            prevClick = this;
        },
        events: events
    })
});
