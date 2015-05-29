var requestReactor = (function($HMU, React, $, _) {

    var should_display = $HMU.should_display && !($HMU.is_user);
    var EventForm = React.createClass({
        handleSubmit: function(e) {
            e.preventDefault();
        },

        render: function() {
            return (
                <div className ="panel panel-default">
                    <h4 id="request-header" align="center"><i className="fa fa-coffee"></i>&nbsp; Send event request</h4>
                    <form id="event-form" onSubmit={this.handleSubmit}>
                        <InputForm ref="inputForm" />
                    </form>
                </div>
            );
        }
    });

    var EventRequestBox = React.createClass({

        getInitialState: function() {
            return {
                display: should_display
            };
        },

        handleSubmit: function() {
            //Handle the form components.
        },

        render: function() {
           var form = <EventForm ref="request"/>;
           var panel = this.state.display ? form : "";

           return (
                 <div>
                 </div>
           );
       }
    });

    // Renders the event request modal.
    return React.render(
        <EventRequestBox />,
        document.getElementById('request-panel')
    );

})(window.$HMU, window.React, window.jQuery, window._);