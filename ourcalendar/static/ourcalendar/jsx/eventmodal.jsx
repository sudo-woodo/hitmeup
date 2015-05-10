//Error messages when user does not input all required fields.
var EventModalError = React.createClass({
    render: function()  {
        return (
            <div className="alert alert-danger" role="alert">{this.props.children}</div>
        );
    }
});

//Event modal allows for creation of events.  Is shown whenever a user clicks
//a day.  Collects all of the necessary information.
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
            calendar: 'Default'      //Necessary for ajax request
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

            var startMoment = moment(postData.start);
            var endMoment = moment(postData.end);

            if ( endMoment.diff(startMoment, 'days' ) == 1 &&
                 startMoment.hour() == 0 && endMoment.hour() == 0 &&
                 startMoment.minute() == 0 && endMoment.minute() == 0 )  {

                postData.allDay = true;
            }

            //Format the dates to send the ajax request
            postData.start = moment(postData.start).format('YYYY-MM-DD HH:mm');
            postData.end = moment(postData.end).format('YYYY-MM-DD HH:mm');

            //ajax request goes here. Fix this url and function.
            /**
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
            */

            //Reset the states upon submission.
            this.setState({
                title: '',
                start: '',
                end: '',
                description: '',
                location: '',
                errors: []
            });
            $('#create-event-modal').modal('hide');
            if (postData.location.length === 0)
                postData.location = 'No location';
            if (postData.description.length === 0)
                postData.description = 'No description';
            var cal = $('#calendar');
            cal.fullCalendar('renderEvent', postData, true);
            cal.fullCalendar('unselect');
        }
    },

    //Initialize all of the states.
    getInitialState: function()  {
        return {
            title: '',
            start: '',
            end: '',
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
        //Contains necessary error information to display to user.
        var errorBox = this.state.errors.map(function(error) {
           return (
               <EventModalError>
                   {error}
               </EventModalError>
           );
        });

        //Responsible for rendering the event modal which consists of a form containing input fields,
        //and date time pickers for start and end dates.
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
                                <p><input type="text" maxLength="200" className="form-control" placeholder="Title" value={this.state.title} ref="title" onChange={this.handleInput} /></p>
                                <p><DateTimeField ref="datetime" /></p>
                                <p><input type="text" maxLength="200" className="form-control" placeholder="Location" value={this.state.location} ref="location" onChange={this.handleInput} /></p>
                                <p><textArea maxLength="600" className="form-control" placeholder="Description" value={this.state.description} ref="description" onChange={this.handleInput} /></p>
                                <button type="submit" className="btn btn-primary pull-right" id="submit">Save changes</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

//Renders the event modal.
var reactor = React.render(
    <EventModal />,
    document.getElementById('create-event-modal-container')
);
