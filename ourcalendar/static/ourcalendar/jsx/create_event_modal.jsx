var creationReactor = (function(React, $) {
    // Gets a range of the months whose events have been rendered
    var getRenderedMonthsRange = function() {
        var months = Object.keys($HMU.monthlyEvents);
        months.sort();

        return {
            start: moment(months[0] + '-01').startOf('month').format('YYYY-MM-DD HH:mm'),
            end: moment(months[months.length - 1] + '-01').endOf('month').format('YYYY-MM-DD HH:mm')
        }
    };

    // Event modal allows for creation of events.  Is shown whenever a user clicks
    // a day.  Collects all of the necessary information.
    var EventModal = React.createClass({

        handleSubmitSingle: function(data)  {
            data.recurrence_type = 'single';

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

            $.ajax({
                url: '/api/events/',
                type: "POST",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(response) {
                    $('#create-event-modal').modal('hide');

                    var range = getRenderedMonthsRange();

                    // Get all the individual recurring events in the recurrence
                    $.ajax({
                        type: "GET",
                        url: "/api/events/?range_start=" + range.start +
                             "&range_end=" + range.end +
                             "&event_id=" + response.id,
                        success: function(responseEvents) {
                            $('#calendar').fullCalendar('addEventSource', responseEvents['objects']);
                        },
                        error: function(err) {
                            alert("An error occurred, please try again later.");
                            console.log(err);
                        }
                    });
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

            // Error checking for days.  Only done if event is repeat.
            if (this.refs.inputForm.state.repeat)  {
                if (days_of_week == null) {
                    errors.unshift('Days are required for repeating events.');
                }
                //grab the endtime.
                postData.last_event = React.findDOMNode(this.refs.inputForm.refs.repeat.refs.endDate).value.trim();
                if (postData.last_event.length === 0)  {
                    errors.unshift('End date for repeating events is required.');
                    this.refs.inputForm.refs.repeat.refs.endDate.getDOMNode().focus();
                }
                else {
                    postData.last_event = moment(postData.last_event);
                    postData.last_event.hour(23).minute(59);
                    if (!(postData.last_event.isAfter(postData.end))) {
                        errors.unshift('End date for repeating events must be after end time.');
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
                var startMoment = moment(postData.start);
                var endMoment = moment(postData.end);

                // Format the dates to send the ajax request
                postData.start = startMoment.format('YYYY-MM-DD HH:mm');
                postData.end = endMoment.format('YYYY-MM-DD HH:mm');

                // Handle repeat and single separately.
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

        // Initialize all of the states.
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