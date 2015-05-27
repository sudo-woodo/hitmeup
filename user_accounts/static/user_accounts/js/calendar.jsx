var calendarReactor = (function($HMU, React, $, _)  {

    // Special non-integer friend event IDs to prevent conflict with user's events
    var BUSY_ID = "FRIEND_BUSY";
    var FREE_ID = "FRIEND_FREE";

    var user_events = $HMU.user_events;
    var friend_events_busy = $HMU.friend_events;
    var friend_events_free = $.extend(true, [], friend_events_busy);
    var should_display = $HMU.should_display;

    friend_events_busy = friend_events_busy.map(function(event) {
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

    friend_events_free = friend_events_free.map(function(event) {
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
                        user_events,
                        friend_events_free,
                        friend_events_busy
                    ],
                    defaultView: "agendaWeek",
                    allDaySlot: false,
                    scrollTime: "08:00:00",
                    selectable: true,
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
                        if (startPicker.length && endPicker.length) {
                            startPicker.data("DateTimePicker").date(start);
                            endPicker.data("DateTimePicker").date(end);
                        }
                    }
                });
            }
        },

        render: function() {
            var window = this.state.initial ? <NotFriend initial={true} /> :
                this.state.display ? <div ref='cal' id="calendar"></div> : <NotFriend initial={false} />;
            var checkboxes = !this.state.initial && this.state.display && !$HMU.is_user ? <ShowEventOptions /> : "";
            return (
                <div>
                    {checkboxes}
                    {window}
                </div>
            );
        }
    });

    var ShowEventOptions = React.createClass({
        getInitialState: function() {
            return  {
                showSelf: true,
                showFree: true,
                showBusy: true
            };
        },

        // TODO figure out how to get calendar DOM node react-ly
        onChangeSelf: function() {
            $('#calendar').fullCalendar(
                this.state.showSelf ? 'removeEventSource' : 'addEventSource', user_events
            );
            this.setState({showSelf: !this.state.showSelf});
        },

        onChangeFree: function() {
            $('#calendar').fullCalendar(
                this.state.showFree ? 'removeEventSource' : 'addEventSource', friend_events_free
            );
            this.setState({showFree: !this.state.showFree});
        },

        onChangeBusy: function() {
            $('#calendar').fullCalendar(
                this.state.showBusy ? 'removeEventSource' : 'addEventSource', friend_events_busy
            );
            this.setState({showBusy: !this.state.showBusy});
        },

        render: function() {
            return (
                <div id="checkboxes">
                    <label className="checkbox-inline">
                        <input type="checkbox" id="showSelf" checked={this.state.showSelf} onChange={this.onChangeSelf} />
                        Show my events
                    </label>
                    <label className="checkbox-inline">
                        <input type="checkbox" id="showFree" checked={this.state.showFree} onChange={this.onChangeFree} />
                        Show my friend's free times
                    </label>
                    <label className="checkbox-inline">
                        <input type="checkbox" id="showBusy" checked={this.state.showBusy} onChange={this.onChangeBusy} />
                        Show my friend's busy times
                    </label>
                </div>
            );
        }
    });

    return React.render(
        <CalendarWindow />,
        document.getElementById('calendar-window-container')
    );

})(window.$HMU, window.React, window.jQuery, window._);