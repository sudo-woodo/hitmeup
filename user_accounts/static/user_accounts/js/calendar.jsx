var calendarReactor = (function($HMU, React, $, _)  {

    var events = $HMU.user_events;
    var friend_events_busy = $HMU.friend_events;
    var friend_events_free = $.extend(true, [], friend_events_busy);
    var should_display = $HMU.should_display;

    //TODO How safe is it to be setting their id's to 1 and 2?
    //Will this cause problems or is this ok?
    friend_events_busy = friend_events_busy.map(function(event) {
        event.rendering = "background";
        event.id = 1;
        event.color = '#FF0000';
        event.title = "Busy";
        return event;
    });

    friend_events_free = friend_events_free.map(function(event) {
        event.rendering = "inverse-background";
        event.id = 2;
        event.color = '#257e4a';
        event.title = "Free";
        return event;
    });

    $.merge(events, friend_events_busy);
    $.merge(events, friend_events_free);

    var NotFriend = React.createClass({
        render: function()  {
            return(
                <div>
                    <i className="fa fa-lock fa-lg"></i>&nbsp; You must be friends with this user to view their calendar.
                </div>
            );
        }
    });

    var CalendarWindow = React.createClass({

        getInitialState: function() {
            return  {
                display: false
            };
        },

        componentDidMount: function() {
            if (this.state.display) {
                var cal = this.refs.cal.getDOMNode();

                $(cal).fullCalendar({
                    events: events,
                    defaultView: "agendaWeek",
                    allDaySlot: false,
                    scrollTime: "08:00:00",
                    selectable: true,
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay'
                    },
                    select: function(start, end) {
                        $('#start-picker').data("DateTimePicker").date(start);
                        $('#end-picker').data("DateTimePicker").date(end);

                    }
                });
            }
        },

        render: function() {
            if (should_display) {
                this.state.display = true;
            }
            var window = this.state.display ? <div ref='cal' id="calendar"></div> : <NotFriend />;

            return (
                <div>
                    {window}
                </div>
            );
        }
    });

    return React.render(
        <CalendarWindow />,
        document.getElementById('calendar-window-container')
    );

})(window.$HMU, window.React, window.jQuery, window._);