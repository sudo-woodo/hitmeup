var EventModal = React.createClass({

    handleSubmit: function(data)  {
        data.preventDefault();
        var postData = {
            title: React.findDOMNode(this.refs.title).value.trim(),
            start: React.findDOMNode(this.refs.datetime.refs.start).value.trim(),
            end: React.findDOMNode(this.refs.datetime.refs.end).value.trim(),
            location: React.findDOMNode(this.refs.location).value.trim(),
            description: React.findDOMNode(this.refs.description).value.trim()
        }

        // Figure out way to send POST data to server.
        console.log('SUBMIT with data:');
        console.log(postData);

        $('#create-event-modal').modal('hide');
    },

    handleDateSubmit: function(date)  {


    },

    getInitialState: function()  {
        return {
            id: -1,
            title: '',
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

    render: function()  {
        return (
            <div id="create-event-modal" className="modal fade">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 className="modal-title">New Event</h4>
                        </div>
                        <div className="modal-body clearfix">
                            <form id="event-form" onSubmit={this.handleSubmit}>
                                <p><input type="text" className="form-control" placeholder="Title" value={this.state.title} ref="title" onChange={this.handleInput} /></p>
                                <p><DateTimeField ref="datetime" onDateSubmit={this.handleDateSubmit} /></p>
                                <p><input type="text" className="form-control" placeholder="Location" value={this.state.location} ref="location" onChange={this.handleInput} /></p>
                                <p><textArea className="form-control" placeholder="Description" value={this.state.description} ref="description" onChange={this.handleInput}/></p>
                                <button type="submit" className="btn btn-primary pull-right" id="submit">Save changes</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var reactor = React.render(
    <EventModal />,
    document.getElementById('create-event-modal-container')
);
