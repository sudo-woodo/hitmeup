var creationReactor = (function(React, $) {
    // Event modal allows for creation of events.  Is shown whenever a user clicks
    // a day.  Collects all of the necessary information.
    var EventModal = React.createClass({

        handleSubmitSingle: function(data)  {
            // Pass in the post data and give it the other relevant info to make it a single.


        },

        handleSubmitRepeat: function(data)  {
            // Pass in the post data and give it the other relevant info to make it a repeat.
            // Get frequency here.  Since days was obtained for error checking, it will already be in data.
            var frequency = $("#frequency").val();
        },

        // Handle submission of event
        handleSubmit: function(data) {
            var days = $("#days").val();

            data.preventDefault();
            var postData = {
                title: React.findDOMNode(this.refs.inputForm.refs.title).value.trim(),
                start: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.start).value.trim(),
                end: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.end).value.trim(),
                location: React.findDOMNode(this.refs.inputForm.refs.location).value.trim(),
                description: React.findDOMNode(this.refs.inputForm.refs.description).value.trim(),
                calendar: 'Default'
                // Set this later recurrence_type: 'single'
            };

            // Do some refactoring...
            // Do everything that is consistent within both types of events, single and repeat.
            // Then pass that data onto their respective functions, handleSubmitSingle and handleSubmitRepeat.


            // Error checking to ensure user put in required fields.
            var errors = [];

            // Error checking for days in here since we checked for errors before all else. Might
            // want to change this.  Also, couldn't get focus to work.
            if (this.refs.inputForm.state.repeat == true && days == null)  {
                errors.unshift('Days are required for repeated events.');
                 this.refs.inputForm.refs.repeat.refs.days.getDOMNode().focus();
            }

            if (postData.end.length === 0) {
                errors.unshift('End time is required.');
                this.refs.inputForm.refs.datetime.refs.end.getDOMNode().focus();
            }

            if (postData.start.length === 0) {
                errors.unshift('Start time is required.');
                this.refs.inputForm.refs.datetime.refs.start.getDOMNode().focus();
            }

            if (postData.title.length === 0) {
                errors.unshift('Title is required.');
                this.refs.inputForm.refs.title.getDOMNode().focus();
            }

            if (errors.length > 0)  {
                this.setState({
                    errors: errors
                });
            }
            else {
                //In here we can change it to handle for single and handle for repeat.

                var startMoment = moment(postData.start);
                var endMoment = moment(postData.end);

                // Format the dates to send the ajax request
                postData.start = startMoment.format('YYYY-MM-DD HH:mm');
                postData.end = endMoment.format('YYYY-MM-DD HH:mm');

                // AJAX request goes here.
                $.ajax({
                    url: '/api/events/',
                    type: "POST",
                    data: JSON.stringify(postData),
                    contentType: "application/json",
                    success: function(response) {
                        postData.id = response.id;
                        $('#create-event-modal').modal('hide');
                        $('#calendar').fullCalendar('renderEvent', postData, true);
                    },
                    error: function (xhr, textStatus, thrownError) {
                        alert("An error occurred, please try again later.");
                        console.log(xhr.responseText);
                    }
                });

            }
        },

        componentDidMount: function()  {
            // Reset min, max dates when event creation modal is dismissed
            $('#create-event-modal').on('hidden.bs.modal', function (e) {
                $('#start-picker').data("DateTimePicker").maxDate(false);
                $('#end-picker').data("DateTimePicker").minDate(false);
                $('#event-form').trigger('reset');
                $('#calendar').fullCalendar('unselect');
            });
        },

        // Initialize all of the states. These are separate from inputForm.  Do they still need
        // to be reset like this?  What can be done differently?
        getInitialState: function()  {
            // Reset the error box.
            return {
                errors: []
            };
        },

        render: function()  {
            // Contains necessary error information to display to user.
            var errorBox = this.state.errors.map(function(error) {
               return (
                   <EventModalError>
                       {error}
                   </EventModalError>
               );
            });

            // Responsible for rendering the event modal which consists of a form containing input fields,
            // and date time pickers for start and end dates.
            return (
                <div id="create-event-modal" className="modal fade" tabIndex="-1">
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
                                    <InputForm ref="inputForm" edit="false" />
                                    <button type="submit" className="btn btn-primary pull-right" id="submit">Save Changes</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    });

    // Renders the event modal.
    return React.render(
        <EventModal />,
        document.getElementById('create-event-modal-container')
    );
})(window.React, window.jQuery);