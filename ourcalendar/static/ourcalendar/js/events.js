(function($, $HMU, _) {
    var monthlyEvents = {};

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
                if (event.recurrence_type === 'weekly')  {
                    revertFunc();
                    alert("We currently do not support editing of repeat events.");
                }
                else {
                    $.ajax({
                        url: '/api/events/' + event.id + '/',
                        type: "PUT",
                        data: JSON.stringify({
                            start: event.start.format('YYYY-MM-DD HH:mm'),
                            end: event.end.format('YYYY-MM-DD HH:mm')
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
                }
            },

            eventResize: function(event, delta, revertFunc)  {
                if ( event.recurrence_type === 'weekly')  {
                    revertFunc();
                    alert("We currently do not support editing of repeat events.");
                }
                else {
                    // Currently the recurrence_type is undefined...Doesn't seem to be a part of the event object.
                    console.log(event.recurrence_type);
                    console.log(event);

                    $.ajax({
                        url: '/api/events/' + event.id + '/',
                        type: "PUT",
                        data: JSON.stringify({
                            start: event.start.format('YYYY-MM-DD HH:mm'),
                            end: event.end.format('YYYY-MM-DD HH:mm')
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
                }
            },

            viewRender: function(view, element) {
                var beginMonth = view.start.format('YYYY-MM');
                var endMonth = view.end.format('YYYY-MM');

                // Begin month's events have not been retrieved yet
                if (!_.has(monthlyEvents, beginMonth)) {
                    var beginRange = view.start.startOf('month').format('YYYY-MM-DD HH:mm');
                    var endRange = view.start.endOf('month').format('YYYY-MM-DD HH:mm');

                    $.ajax({
                        url: '/api/events/?range_start=' + beginRange + '&range_end=' + endRange,
                        type: "GET",
                        contentType: "application/json",
                        success: function (response) {
                            $('#calendar').fullCalendar('addEventSource', response['objects']);
                            monthlyEvents[beginMonth] = true;
                        },
                        error: function (xhr, textStatus, thrownError) {
                            alert("An error occurred, please try again later.");
                            console.log(xhr.responseText);
                        }
                    });
                }

                // End month's events have not been retrieved yet
                if (!_.has(monthlyEvents, endMonth)) {
                    beginRange = view.end.startOf('month').format('YYYY-MM-DD HH:mm');
                    endRange = view.end.endOf('month').format('YYYY-MM-DD HH:mm');

                    $.ajax({
                        url: '/api/events/?range_start=' + beginRange + '&range_end=' + endRange,
                        type: "GET",
                        contentType: "application/json",
                        success: function (response) {
                            $('#calendar').fullCalendar('addEventSource', response['objects']);
                            monthlyEvents[endMonth] = true;
                        },
                        error: function (xhr, textStatus, thrownError) {
                            alert("An error occurred, please try again later.");
                            console.log(xhr.responseText);
                        }
                    });
                }
            }
        });

        // Initial load of current month's events
        var beginRange = moment().startOf('month').format('YYYY-MM-DD HH:mm');
        var endRange = moment().endOf('month').format('YYYY-MM-DD HH:mm');
        $.ajax({
            url: '/api/events/?range_start=' + beginRange + '&range_end=' + endRange,
            type: "GET",
            contentType: "application/json",
            success: function (response) {
                $('#calendar').fullCalendar('addEventSource', response['objects']);
                monthlyEvents[moment().format('YYYY-MM')] = true;
            },
            error: function (xhr, textStatus, thrownError) {
                alert("An error occurred, please try again later.");
                console.log(xhr.responseText);
            }
        });
    });
})(window.jQuery, window.$HMU, window._);