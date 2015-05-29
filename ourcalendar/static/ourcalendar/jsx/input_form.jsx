// This will be the react class used as the input form for creation and editing of an event.
// for use in both the event detail modal and the create event modal.
var InputForm = (function(React, $)  {

    return React.createClass({

        // State in regards to the frequency and days of repetition are held in create_event_modal
        // since they accessed using jQuery.
        getInitialState: function()  {
            return  {
                title: '',
                start: '',
                end: '',
                description: '',
                location: '',
                repeat: false
            };
        },

        componentDidMount: function()  {
            $("[name='repeat']").bootstrapSwitch({
                onSwitchChange: this.onChangeRepeat,
                size: 'normal',
                labelText: "repeat",
                handleWidth: 50
            });
        },

        onChangeRepeat: function()  {
            this.setState({repeat: !this.state.repeat});
        },

        handleInput: function()  {
            this.setState({
                title: this.refs.title.getDOMNode().value,
                description: this.refs.description.getDOMNode().value,
                location: this.refs.location.getDOMNode().value
            });
        },

        // Returns fields that are then put into the form.
        render: function()  {
            // This is so that this will be used only for creation.  Don't worry about editing an event to add repetiton for now
            var isCreation = false;
            if (this.props.edit == "false")  {
                isCreation = true;
            }
            var repeatBox = (this.state.repeat && isCreation) ? <RepeatBox ref="repeat"/> : "";
            var repeatButton = (this.state.repeat && isCreation) ? <p><input id="repeat" name="repeat" type="checkbox" checked={this.state.repeat} /></p> : "";

            return (
                <div>
                    <p><input type="text" maxLength="200" className="form-control" placeholder="Title" value={this.state.title} ref="title" onChange={this.handleInput} /></p>
                    <p><DateTimeField ref="datetime" /></p>
                    {repeatButton}
                    <p>{repeatBox}</p>
                    <p><input type="text" maxLength="200" className="form-control" placeholder="Location" value={this.state.location} ref="location" onChange={this.handleInput} /></p>
                    <p><textArea maxLength="600" className="form-control" placeholder="Description" value={this.state.description} ref="description" onChange={this.handleInput} /></p>
                </div>
            );
        }
    });
})(window.React, window.jQuery);
