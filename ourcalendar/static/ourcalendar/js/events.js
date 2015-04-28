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
            },
            events: events
        })
    });
})(window.jQuery, $HMU);