(function($, $HMU) {
    var events = $.map($HMU.calendars, function(c) {
        return c;
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
                $("#myModal").modal('show');
            },
            eventClick: function(event) {
                // Use event.id to get the clicked event's id
                $('#eventDetailModal .modal-title').text(event.title);
                $('#eventDetailModal #start-time').text(moment(event.start).format('LLL'));
                $('#eventDetailModal #end-time').text(moment(event.end).format('LLL'));
                $('#eventDetailModal #location').text(event.location);
                $('#eventDetailModal #description').text(event.description);
                $('#eventDetailModal').modal('show');
            },
            events: events,
            fixedWeekCount: false,
            height: 600,
            scrollTime: "08:00:00"
        })
    });
})(window.jQuery, $HMU);