// This will be the react class used as the input form for creation and editing of an event.
// for use in both the event detail modal and the create event modal.
var InputForm = (function(React, $)  {

    return React.createClass({

        getInitialState: function()  {
            return  {
                title: '',
                start: '',
                end: '',
                description: '',
                location: ''
            };
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
            return (
                <div id="request-form">
                    <p><input type="text" maxLength="200" className="form-control" placeholder="Title" value={this.state.title} ref="title" onChange={this.handleInput} /></p>
                    <p><DateTimeField ref="datetime" /></p>
                    <p><input type="text" maxLength="200" className="form-control" placeholder="Location" value={this.state.location} ref="location" onChange={this.handleInput} /></p>
                    <p><textArea maxLength="600" className="form-control" placeholder="Description" value={this.state.description} ref="description" onChange={this.handleInput} /></p>
                    <button type="submit" className="btn btn-primary pull-right" id="submit">Send Request</button>
                </div>
            );
        }
    });
})(window.React, window.jQuery);
