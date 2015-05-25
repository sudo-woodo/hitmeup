var calendarReactor = (function($HMU, React, $, _)  {

    var events = $HMU.user_events;
    var friend_events = $HMU.friend_events;
    var should_display = $HMU.should_display;

    friend_events = friend_events.map(function(event) {
        event.rendering = "inverse-background";
        event.id = 1;
        event.color = '#257e4a';
        event.title = "Busy";
        return event;
    });

    $.merge(events, friend_events);

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