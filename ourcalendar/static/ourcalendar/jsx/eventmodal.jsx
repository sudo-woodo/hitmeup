var EventModal = React.createClass({

    handleSubmit: function(data)  {
        data.preventDefault();
        var title = React.findDOMNode(this.refs.title).value.trim();
        var description = React.findDOMNode(this.refs.description).value.trim();

        //Figure out way to sent data to server.

    },

    handleDateSubmit: function(date)  {


    },

    getInitialState: function()  {
        return {
            id: -1,
            title: '',
            description: ''
        };
    },

    handleInput: function()  {
        this.setState({
            title: this.refs.title.getDOMNode().value,
            description: this.refs.description.getDOMNode().value
        });
    },

    render: function()  {
        return (
            <div id="create-event-modal" className="modal fade">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 className="modal-title">Event Creation</h4>
                        </div>
                        <div className="modal-body">
                            <form id="event-form" onSubmit={this.handleSubmit}>
                                <p><input type="text" placeholder="Title" value={this.state.title} ref="title" onChange={this.handleInput} /></p>
                                <p><input type="text" placeholder="Description" value={this.state.description} ref="description" onChange={this.handleInput}/></p>
                                <p><DateTimeField onDateSubmit={this.handleDateSubmit} /></p>
                                <p><DateTimeField placeholder="End time" /></p>
                            </form>


                            <p>Click save changes to save event to your calendar.</p>
                            <p class="text-warning"><small>If you don't save, your changes will be lost.</small></p>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
                            <button type="button" className="btn btn-primary">Save changes</button>
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
