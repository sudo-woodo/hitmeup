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
                $("#create-event-modal").modal('show');
                $("#create-event-modal").on('hide.bs.modal', function () {
                    $(this).find('form')[0].reset();
                });
            },
            eventClick: function(event) {
                $('#eventDetailModal .modal-title').text(event.title + ' (' + event.id + ')');
                $('#eventDetailModal .modal-title').css('color', event.color);
                $('#eventDetailModal .label').css('background-color', event.color);
                $('#eventDetailModal #start-time').text(moment(event.start).format('LLL'));
                $('#eventDetailModal #end-time').text(moment(event.end).format('LLL'));
                $('#eventDetailModal #cal-title').text(event.calendar);
                $('#eventDetailModal #location').text(event.location);
                $('#eventDetailModal #description').text(event.description);
                $('#eventDetailModal #attendees').text(event.users ? event.users : 'No one yet!');
                $('#eventDetailModal').modal('show');
            },
            events: events,
            fixedWeekCount: false,
            height: 600,
            scrollTime: "08:00:00"
        })
    });
})(window.jQuery, $HMU);

