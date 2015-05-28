var calendarReactor = (function($HMU, React, $, _)  {

    // Special non-integer friend event IDs to prevent conflict with user's events
    var BUSY_ID = "FRIEND_BUSY";
    var FREE_ID = "FRIEND_FREE";

    var friend_events_busy = $HMU.friend_events;
    var friend_events_free = $.extend(true, [], friend_events_busy);
    var should_display = $HMU.should_display;

    $HMU.friend_events_busy = friend_events_busy.map(function(event) {
        event.rendering = "background";
        event.id = BUSY_ID;
        event.color = '#FF0000';
        event.title = "Busy";
        return event;
    });

    // If viewing friend profile and friend has no events, friend is free at all times
    if (!$HMU.is_user && friend_events_free.length === 0) {
        var currTime = moment();
        friend_events_free.push({
            start: currTime,
            end: currTime
        });
    }

    $HMU.friend_events_free = friend_events_free.map(function(event) {
        event.rendering = "inverse-background";
        event.id = FREE_ID;
        event.color = '#257e4a';
        event.title = "Free";
        return event;
    });

    var NotFriend = React.createClass({
        render: function()  {
            var icon = this.props.initial ? "fa fa-refresh fa-lg" : "fa fa-lock fa-lg";
            var message = this.props.initial ?
                "Please refresh this page to view their calendar." :
                "You must be friends with this user to view their calendar.";
            return(
                <div>
                    <i className={icon}></i>&nbsp; {message}
                </div>
            );
        }
    });

    var CalendarWindow = React.createClass({

        getInitialState: function() {
            return  {
                display: should_display,
                initial: false
            };
        },

        componentDidMount: function() {
            if (this.state.display) {
                var cal = this.refs.cal.getDOMNode();

                $(cal).fullCalendar({
                    eventSources: [
                        $HMU.user_events,
                        $HMU.friend_events_free,
                        $HMU.friend_events_busy
                    ],
                    defaultView: "agendaWeek",
                    allDaySlot: false,
                    scrollTime: "08:00:00",
                    defaultTimedEventDuration: "00:00:00",
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay'
                    },
                    select: function(start, end) {
                        var startPicker = $('#start-picker');
                        var endPicker = $('#end-picker');

                        // jQuery element's length is > 0 if it exists
                        // TODO bug: start picker updates only like 50% of the time...
                        if (startPicker.length && endPicker.length) {
                            startPicker.data("DateTimePicker").date(start);
                            endPicker.data("DateTimePicker").date(end);
                        }
                    }
                });
            }
        },

        render: function() {
            var calendar = <NotFriend initial={true} />;
            if (!this.state.initial) {
                if (this.state.display)
                    calendar = <div ref='cal' id="calendar"></div>;
                else
                    calendar = <NotFriend initial={false} />;
            }

            return (
                <div>
                    {calendar}
                </div>
            );
        }
    });

    return React.render(
        <CalendarWindow />,
        document.getElementById('calendar-window-container')
    );

})(window.$HMU, window.React, window.jQuery, window._);