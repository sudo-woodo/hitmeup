//Error messages when user does not input all required fields.
var EventModalError = React.createClass({
    render: function()  {
        return (
            <div className="alert alert-danger" role="alert">{this.props.children}</div>
        );
    }
});


var EventModal = React.createClass({

    //handle submission of event
    handleSubmit: function(data) {
        data.preventDefault();
        var postData = {
            title: React.findDOMNode(this.refs.title).value.trim(),
            start: React.findDOMNode(this.refs.datetime.refs.start).value.trim(),
            end: React.findDOMNode(this.refs.datetime.refs.end).value.trim(),
            location: React.findDOMNode(this.refs.location).value.trim(),
            description: React.findDOMNode(this.refs.description).value.trim(),
            calendar: 'Default'
        };

        // Figure out way to send POST data to server.
        console.log('SUBMIT with data:');
        console.log(postData);

        //Error checking to ensure user put in required fields.
        var arr = [];
        if (postData.end.length === 0 )  {
            arr.unshift('End time is required.');
            this.refs.datetime.refs.end.getDOMNode().focus();
        }
        if (postData.start.length === 0 )  {
            arr.unshift('Start time is required.');
            this.refs.datetime.refs.start.getDOMNode().focus();
        }
        if (postData.title.length === 0 ) {
            arr.unshift('Title is required.');
            this.refs.title.getDOMNode().focus();
        }

        if (arr.length > 0 )  {
            this.setState({
                errors: arr
            });
        }
        else {
            //Format the dates to send the ajax request
            postData.start = moment(postData.start).format('YYYY-MM-DD hh:mm');
            postData.end = moment(postData.end).format('YYYY-MM-DD hh:mm');

            //ajax request goes here. Fix this url and function.
            $.ajax({
                url: '/api/events/',
                type: "POST",
                data: JSON.stringify(postData),
                contentType: "application/json",
                success:function(response){},
                complete:function(){},
                error:function (xhr, textStatus, thrownError){
                    console.log(xhr.responseText);
                }
                
            });

            //Reset the states upon submission.
            this.setState({
                title: '',
                description: '',
                location: '',
                errors: []
            });
            $('#create-event-modal').modal('hide');
        }
    },


    getInitialState: function()  {
        return {
            title: '',
            description: '',
            location: '',
            errors: []

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
        var errorBox = this.state.errors.map(function(error) {
           return (
               <EventModalError>
                   {error}
               </EventModalError>
           );

        });


        return (
            <div id="create-event-modal" className="modal fade">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 className="modal-title">New Event</h4>
                        </div>
                        <div className="modal-body clearfix">
                            <div>
                                {errorBox}
                            </div>
                            <form id="event-form" onSubmit={this.handleSubmit}>
                                <p><input type="text" className="form-control" placeholder="Title" value={this.state.title} ref="title" onChange={this.handleInput} /></p>
                                <p><DateTimeField ref="datetime" /></p>
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
