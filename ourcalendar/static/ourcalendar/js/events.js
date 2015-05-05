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
                 /*               // using jQuery
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                var csrftoken = getCookie('csrftoken');
                function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                }
                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });*/

                $.ajax({
                    url:'/calendar/api/events/',
                    type: "POST",
                    data: JSON.stringify({title: 'a', start: '2015-05-29 12:12',
                        end: '1990-12-12 12:13', calendar:'Default',
                        description: 'new des', location: ''}),
                    contentType: "application/json",
                    success:function(response){},
                    complete:function(){},
                    error:function (xhr, textStatus, thrownError){
                        console.log(xhr.responseText);
                    }
                });
                //$("#myModal").modal('show');
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