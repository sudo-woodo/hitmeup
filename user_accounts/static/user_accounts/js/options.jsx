var optionsReactor = (function($HMU, React, $, _) {

    var Checkboxes = React.createClass({
        getInitialState: function() {
            return  {
                showSelf: true,
                showFree: true,
                showBusy: true
            };
        },

        componentDidMount: function() {
            $("[name='showSelf']").bootstrapSwitch({
                onSwitchChange: this.onChangeSelf,
                size: 'normal',
                labelText: "events",
                handleWidth: 50
            });
            $("[name='showFree']").bootstrapSwitch({
                onSwitchChange: this.onChangeFree,
                size: 'normal',
                labelText: "free",
                handleWidth: 50
            });
            $("[name='showBusy']").bootstrapSwitch({
                onSwitchChange: this.onChangeBusy,
                size: 'normal',
                labelText: "busy",
                handleWidth: 50
            });
        },

        onChangeSelf: function() {
            $('#calendar').fullCalendar(
                this.state.showSelf ? 'removeEventSource' : 'addEventSource', $HMU.user_events
            );
            this.setState({showSelf: !this.state.showSelf});
        },

        onChangeFree: function() {
            $('#calendar').fullCalendar(
                this.state.showFree ? 'removeEventSource' : 'addEventSource', $HMU.friend_events_free
            );
            this.setState({showFree: !this.state.showFree});
        },

        onChangeBusy: function() {
            $('#calendar').fullCalendar(
                this.state.showBusy ? 'removeEventSource' : 'addEventSource', $HMU.friend_events_busy
            );
            this.setState({showBusy: !this.state.showBusy});
        },

        render: function() {
            return (
                <div className="panel panel-default">
                    <div id="option-label">Show my events</div>
                    <div>
                        <input type="checkbox" name="showSelf" id="showSelf" checked={this.state.showSelf} />
                    </div>
                    <div id="option-label">Show friend's events</div>
                    <div>
                        <input type="checkbox" name="showFree" id="showFree" checked={this.state.showFree} />
                    </div>
                    <div>
                        <input type="checkbox" name="showBusy" id="showBusy" checked={this.state.showBusy} />
                    </div>
                </div>
            );
        }
    });

    var ShowEventOptions = React.createClass({
        getInitialState: function() {
            return  {
                display: true
            };
        },
        render: function() {
            var checkboxes = this.state.display && $HMU.should_display && !$HMU.is_user ? <Checkboxes /> : null;
            return (
                <div>
                    {checkboxes}
                </div>
            );
        }
    });

    // Renders the event request modal.
    return React.render(
        <ShowEventOptions />,
        document.getElementById('options-panel')
    );

})(window.$HMU, window.React, window.jQuery, window._);