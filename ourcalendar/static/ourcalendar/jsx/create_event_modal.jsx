var creationReactor = (function(React, $) {
    // Event modal allows for creation of events.  Is shown whenever a user clicks
    // a day.  Collects all of the necessary information.
    var EventModal = React.createClass({

        handleSubmitSingle: function(data)  {
            // Pass in the post data and give it the other relevant info to make it a single.
            data.recurrence_type = 'single';

            // AJAX request goes here.
            $.ajax({
                url: '/api/events/',
                type: "POST",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(response) {
                    $('#create-event-modal').modal('hide');
                    $('#calendar').fullCalendar('renderEvent', response, true);
                },
                error: function (xhr, textStatus, thrownError) {
                    alert("An error occurred, please try again later.");
                    console.log(xhr.responseText);
                }
            });

        },

        handleSubmitRepeat: function(data)  {
            // Pass in the post data and give it the other relevant info to make it a repeat.
            // Get frequency here.  Since days was obtained for error checking, it will already be in data.
            var frequency = $("#frequency").val();
            data.frequency = 1;   // By default frequency is weekly.
            if ( frequency != null ) {
                data.frequency = frequency[0];
            }

            data.recurrence_type = 'weekly';
            data.last_event = data.last_event.format('YYYY-MM-DD HH:mm');

            // Represents the days of the week selected by the user. 1 indicates they selected the day.
            var days_of_week = ['0', '0', '0', '0', '0', '0', '0'];
            for (var i = 0; i < data.days_of_week.length; i++ )  {
                days_of_week[data.days_of_week[i]] = '1';
            }
            data.days_of_week = days_of_week.join("");

            // AJAX request goes here.
            $.ajax({
                url: '/api/events/',
                type: "POST",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(response) {
                    // what to do with id.
                    $('#create-event-modal').modal('hide');
                    $('#calendar').fullCalendar('renderEvent', response, true);
                },
                error: function (xhr, textStatus, thrownError) {
                    alert("An error occurred, please try again later.");
                    console.log(xhr.responseText);
                }
            });
        },

        // Handle submission of event
        handleSubmit: function(data) {
            var days_of_week = $("#days").val();

            data.preventDefault();
            var postData = {
                title: React.findDOMNode(this.refs.inputForm.refs.title).value.trim(),
                start: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.start).value.trim(),
                end: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.end).value.trim(),
                location: React.findDOMNode(this.refs.inputForm.refs.location).value.trim(),
                description: React.findDOMNode(this.refs.inputForm.refs.description).value.trim(),
                calendar: 'Default'
            };

            // Error checking to ensure user put in required fields.
            var errors = [];

            // Error checking for days in here since we checked for errors before all else. Might
            // want to change this.  Also, couldn't get focus to work.
            if (this.refs.inputForm.state.repeat)  {
                if (days_of_week == null) {
                    errors.unshift('Days are required for repeated events.');
                    // this.refs.inputForm.refs.repeat.refs.days.getDOMNode().focus();
                }
                //grab the endtime.
                postData.last_event = React.findDOMNode(this.refs.inputForm.refs.repeat.refs.endDate).value.trim();
                console.log("length of endDate " + postData.last_event.length);
                if (postData.last_event.length === 0)  {
                    errors.unshift('End date for repeat events is required');
                    this.refs.inputForm.refs.repeat.refs.endDate.getDOMNode().focus();
                }
                else {
                    console.log( "before ");
                    console.log( postData.last_event );
                    postData.last_event = moment(postData.last_event);
                    console.log( "after moment" );
                    console.log( postData.last_event );
                    postData.last_event.hour(23).minute(53);
                    console.log( "after adding time ");
                    console.log( postData.last_event );
                    if (!(postData.last_event.isAfter(postData.end))) {
                        errors.unshift('End date for repeat events must be after end time');
                        this.refs.inputForm.refs.repeat.refs.endDate.getDOMNode().focus();
                    }
                }
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

                if (this.refs.inputForm.state.repeat) {
                    postData.days_of_week = days_of_week;
                    this.handleSubmitRepeat(postData);
                }
                else {
                    this.handleSubmitSingle(postData);
                }
            }
        },

        componentDidMount: function() {
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