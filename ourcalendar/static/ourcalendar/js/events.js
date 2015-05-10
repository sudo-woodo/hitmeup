(function($, $HMU) {
    var events = $.map($HMU.calendars, function(c) {
        return c;
    });

    $(document).ready(function() {

        //Displays the calendar.
        $('#calendar').fullCalendar({
            editable: true,
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },

            //Shows detail when clicking an event.
            eventClick: function(event) {
                // Use event.id to get the clicked event's id
                $('#eventDetailModal .modal-title').text(event.title);

                if ( event.allDay == false )  {
                    $('#eventDetailModal #start-time').text(moment(event.start).format('LLL'));
                    $('#eventDetailModal #start-time').append(' -')
                    $('#eventDetailModal #end-time').text(moment(event.end).format('LLL'));
                }
                else  {
                    $('#eventDetailModal #start-time').text(moment(event.start).format('LL'));
                    $('#eventDetailModal #end-time').text("");
                }
                $('#eventDetailModal #location').text(event.location);
                $('#eventDetailModal #description').text(event.description);
                $('#eventDetailModal').modal('show');
            },
            events: events,
            fixedWeekCount: false,
            height: 600,
            scrollTime: "08:00:00",
            selectable: true,
            eventLimit: true,
            selectHelper: true,
            unselectCancel: "#create-event-modal",
            select: function(start, end) {
                $('#start-picker').data("DateTimePicker").date(start);
                $('#end-picker').data("DateTimePicker").date(end);
                reactor.setState(reactor.getInitialState());
                $("#create-event-modal").modal('show');
            },

            forceEventDuration: true

        })
    });
})(window.jQuery, $HMU);

