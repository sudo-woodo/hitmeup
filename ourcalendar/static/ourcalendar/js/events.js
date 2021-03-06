(function($, $HMU, _) {
    $HMU.monthlyEvents = {};

    $(document).ready(function() {

        // Displays the calendar.
        $('#calendar').fullCalendar({
            editable: true,
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },

            // Shows detail when clicking an event.
            eventClick: function(event) {
                detailReactor.setState({
                    edit: false,
                    title: event.title,
                    location: event.location,
                    description: event.description,
                    start: event.start.format('LLL'),
                    end: event.end.format('LLL'),
                    id: event.id,
                    repeat: event.recurrence_type
                });

                // Dev tip: can use event.id to get the clicked event's id
                $('#eventDetailModal').modal('show');
            },
            fixedWeekCount: false,
            defaultView: "agendaWeek",
            height: 600,
            scrollTime: "08:00:00",
            selectable: true,
            eventLimit: true,
            selectHelper: true,
            unselectCancel: "#create-event-modal",
            select: function(start, end) {
                $('#start-picker').data("DateTimePicker").date(start);
                $('#end-picker').data("DateTimePicker").date(end);

                // Reset the state of both the create event modal and the input form.
                creationReactor.setState(creationReactor.getInitialState());
                creationReactor.refs.inputForm.setState(creationReactor.refs.inputForm.getInitialState());

                $("#create-event-modal").modal('show');
            },
            forceEventDuration: true,
            allDaySlot: false,

            eventDrop: function(event, delta, revertFunc)  {
                $.ajax({
                    url: '/api/events/' + event.id + '/',
                    type: "PUT",
                    data: JSON.stringify({
                        start: event.start.format('YYYY-MM-DD HH:mm'),
                        end: event.end.format('YYYY-MM-DD HH:mm'),
                        recurrence_type: event.recurrence_type,
                        start_delta: delta.asMilliseconds(),
                        end_delta: delta.asMilliseconds()
                    }),
                    contentType: "application/json",
                    success: function (response) {
                    },
                    complete: function () {
                    },
                    error: function (xhr, textStatus, thrownError) {
                        revertFunc();
                        alert("An error occurred, please try again later.");
                        console.log(xhr.responseText);
                    }
                });
            },

            eventResize: function(event, delta, revertFunc)  {
                $.ajax({
                    url: '/api/events/' + event.id + '/',
                    type: "PUT",
                    data: JSON.stringify({
                        start: event.start.format('YYYY-MM-DD HH:mm'),
                        end: event.end.format('YYYY-MM-DD HH:mm'),
                        recurrence_type: event.recurrence_type,
                        start_delta: 0,
                        end_delta: delta.asMilliseconds()
                    }),
                    contentType: "application/json",
                    success: function (response) {
                    },
                    complete: function () {
                    },
                    error: function (xhr, textStatus, thrownError) {
                        revertFunc();
                        alert("An error occurred, please try again later.");
                        console.log(xhr.responseText);
                    }
                });
            },

            viewRender: function(view, element) {
                var beginMonth = view.start.format('YYYY-MM');
                var currMonth = view.intervalStart.format('YYYY-MM');
                var endMonth = view.end.format('YYYY-MM');

                // Begin month's events have not been retrieved yet
                if (!_.has($HMU.monthlyEvents, beginMonth)) {
                    var beginRangePrev = view.start.startOf('month').format('YYYY-MM-DD HH:mm');
                    var endRangePrev = view.start.endOf('month').format('YYYY-MM-DD HH:mm');

                    $.ajax({
                        url: '/api/events/?range_start=' + beginRangePrev + '&range_end=' + endRangePrev,
                        type: "GET",
                        contentType: "application/json",
                        success: function (response) {
                            $('#calendar').fullCalendar('addEventSource', response['objects']);
                        },
                        error: function (xhr, textStatus, thrownError) {
                            alert("An error occurred, please try again later.");
                            console.log(xhr.responseText);
                        }
                    });
                    $HMU.monthlyEvents[beginMonth] = true;
                }

                // End month's events have not been retrieved yet
                if (!_.has($HMU.monthlyEvents, currMonth)) {
                    var beginRangeCurr = view.intervalStart.startOf('month').format('YYYY-MM-DD HH:mm');
                    var endRangeCurr = view.intervalStart.endOf('month').format('YYYY-MM-DD HH:mm');

                    $.ajax({
                        url: '/api/events/?range_start=' + beginRangeCurr + '&range_end=' + endRangeCurr,
                        type: "GET",
                        contentType: "application/json",
                        success: function (response) {
                            $('#calendar').fullCalendar('addEventSource', response['objects']);
                            $HMU.monthlyEvents[endMonth] = true;
                        },
                        error: function (xhr, textStatus, thrownError) {
                            alert("An error occurred, please try again later.");
                            console.log(xhr.responseText);
                        }
                    });
                    $HMU.monthlyEvents[currMonth] = true;
                }

                // End month's events have not been retrieved yet
                if (!_.has($HMU.monthlyEvents, endMonth)) {
                    var beginRangeNext = view.end.startOf('month').format('YYYY-MM-DD HH:mm');
                    var endRangeNext = view.end.endOf('month').format('YYYY-MM-DD HH:mm');

                    $.ajax({
                        url: '/api/events/?range_start=' + beginRangeNext + '&range_end=' + endRangeNext,
                        type: "GET",
                        contentType: "application/json",
                        success: function (response) {
                            $('#calendar').fullCalendar('addEventSource', response['objects']);
                            $HMU.monthlyEvents[endMonth] = true;
                        },
                        error: function (xhr, textStatus, thrownError) {
                            alert("An error occurred, please try again later.");
                            console.log(xhr.responseText);
                        }
                    });
                    $HMU.monthlyEvents[endMonth] = true;
                }
            }
        });
    });
})(window.jQuery, window.$HMU, window._);