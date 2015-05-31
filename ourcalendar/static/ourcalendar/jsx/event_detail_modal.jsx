var detailReactor = (function(React, $) {
    // Default event details including the description and location.
    var DefaultDetail = React.createClass({
        render: function()  {
            var location_text = this.props.location.length == 0 ? "No location" : this.props.location;
            var description_text = this.props.description.length == 0 ? "No description" : this.props.description;

            return (
                <div id="desc-loc-container">
                    <ul className="fa-ul">
                        <li><i className="fa-li fa fa-map-marker"></i><span id="location">{location_text}</span></li>
                        <li><i className="fa-li fa fa-calendar"></i><span id="description">{description_text}</span></li>
                    </ul>
                </div>
            );
        }
    });

    var EventDetailModal = React.createClass({

        componentDidUpdate: function()  {
            //If edit is now true, update the inputForm.
            if ( this.state.edit == true ) {
                this.refs.inputForm.setState({
                    title: this.state.title,
                    location: this.state.location,
                    description: this.state.description,
                    start: this.state.start,
                    end: this.state.end
                });

                $(this.refs.inputForm.refs.datetime.refs.startpicker.getDOMNode())
                    .data("DateTimePicker").date(moment(this.state.start));
                $(this.refs.inputForm.refs.datetime.refs.endpicker.getDOMNode())
                    .data("DateTimePicker").date(moment(this.state.end));

                this.refs.inputForm.refs.datetime.setState({
                   repeat: this.state.repeat === 'weekly'
                });
            }
        },

        // On edit, set edit state to true and render the form.
        handleEdit: function()  {
            this.setState({
                edit: true,
                errors: []
            });
        },

        // User presses delete button, deletes event and renders the calendar.
        handleDelete: function()  {
            // AJAX request to delete event.
            $.ajax({
                    url: '/api/events/' + this.state.id + '/',
                    type: "DELETE",
                    contentType: "application/json",
                    success: function (response) {
                        $('#calendar').fullCalendar('removeEvents', this.state.id);
                        $('#eventDetailModal').modal('hide');
                    }.bind(this),
                    error: function (xhr, textStatus, thrownError) {
                        alert("An error occurred, please try again later.");
                        console.log(xhr.responseText);
                    }
                });
        },

        // User presses submit, sends AJAX request with required data. Ensures data is valid first.
        handleSubmit: function()  {
            var putData = {
                title: React.findDOMNode(this.refs.inputForm.refs.title).value.trim(),
                start: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.start).value.trim(),
                end: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.end).value.trim(),
                location: React.findDOMNode(this.refs.inputForm.refs.location).value.trim(),
                description: React.findDOMNode(this.refs.inputForm.refs.description).value.trim(),
                calendar: 'Default',      // Necessary for AJAX request
                recurrence_type: this.state.repeat
            };

            // Error checking: title, start, and end times all required.
            var errors = [];
            if (putData.end.length === 0) {
                errors.unshift('End time is required.');
                this.refs.inputForm.refs.datetime.refs.end.getDOMNode().focus();
            }

            if (putData.start.length === 0) {
                errors.unshift('Start time is required.');
                this.refs.inputForm.refs.datetime.refs.start.getDOMNode().focus();
            }

            if (putData.title.length === 0) {
                errors.unshift('Title is required.');
                this.refs.inputForm.refs.title.getDOMNode().focus();
            }

            if (errors.length > 0)  {
                this.setState({
                    errors: errors
                });
            }
            else {
                // These are used to set the resulting event's start and end times.
                var startMoment = moment($(this.refs.inputForm.refs.datetime.refs.startpicker.getDOMNode()).data("DateTimePicker").date());
                var endMoment = moment($(this.refs.inputForm.refs.datetime.refs.endpicker.getDOMNode()).data("DateTimePicker").date());

                putData.start = startMoment.format('YYYY-MM-DD HH:mm');
                putData.end = endMoment.format('YYYY-MM-DD HH:mm');

                // For updating recurring events, need the change in times in milliseconds
                putData.start_delta = startMoment.diff(moment(this.state.start));
                putData.end_delta = endMoment.diff(moment(this.state.end));

                // AJAX request to edit the event
                $.ajax({
                    url: '/api/events/' + this.state.id + '/',
                    type: "PUT",
                    data: JSON.stringify(putData),
                    contentType: "application/json",
                    success: function (response) {
                        var full_calendar = $('#calendar');
                        // Grab the first event and update it
                        var result = full_calendar.fullCalendar('clientEvents', this.state.id)[0];
                        result.title = putData.title;
                        result.start = startMoment;
                        result.end = endMoment;
                        result.description = putData.description;
                        result.location = putData.location;

                        full_calendar.fullCalendar('updateEvent', result);
                        $('#eventDetailModal').modal('hide');
                    }.bind(this),
                    error: function (xhr, textStatus, thrownError) {
                        alert("An error occurred, please try again later.");
                        console.log(xhr.responseText);
                    }
                });
            }
        },

        // User presses cancel button, is returned to previous screen.
        handleCancel: function()  {
            this.setState({
                edit: false,
                errors: []
            });
        },

        // dummy get initial state for the time being.
        getInitialState: function()  {
            return  {
                title: "",
                location: "",
                description: "",
                start: "",
                end: "",
                edit: false,
                id: -1,
                errors: [],
                repeat: ""
            };
        },

        componentDidMount: function()  {
            $('#eventDetailModal').on('hidden.bs.modal', function() {
                this.setState({edit: false});
            }.bind(this));
        },

        render: function()  {
            // This will be the form that will be rendered upon clicking edit button.
            // The Default detail should probably be a larger part including the header of the modal.
            // TODO: ternaries are cool guys, but eventually refactor into 2 components
            var form = this.state.edit ? <InputForm ref="inputForm" edit="true" /> :
                <DefaultDetail location={this.state.location} description={this.state.description} />;
            var edit_submit_button = this.state.edit ? this.handleSubmit : this.handleEdit;
            var edit_submit_text = this.state.edit ? "Save Changes" : "Edit Event";
            var delete_cancel_button = this.state.edit ? this.handleCancel : this.handleDelete;
            var delete_cancel_text = this.state.edit ? "Cancel" : "Delete";
            var delete_cancel_class = this.state.edit ? "btn btn-primary" : "btn btn-danger";
            var repeat_text = this.state.repeat === 'single' ? "One-time" : "Repeating";
            var repeat_icon = this.state.repeat === 'single' ? "fa fa-sun-o" : "fa fa-repeat";

            // Contains all of the info for the errors.  Only displayed while the form is shown.
            var errors = this.state.errors.map(function(error) {
               return (
                   <EventModalError>
                       {error}
                   </EventModalError>
               );
            });
            var display_errors = this.state.edit ? errors : "";

            return(
                <div id="eventDetailModal" className="modal fade" tabIndex="-1">
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                <h3 className="modal-title">{this.state.title}</h3>
                                <i className="fa fa-clock-o"></i>&nbsp;&nbsp;<span id="start-time">{this.state.start}</span> &mdash; <span id="end-time">{this.state.end}</span>
                                <br/>
                                <i className={repeat_icon}></i>&nbsp;&nbsp;<span id="repeat">{repeat_text} event</span>
                            </div>
                            <div className="modal-body">
                                <div>
                                    {display_errors}
                                </div>
                                <form id="edit-form" onSubmit={this.handleSubmit}>
                                    {form}
                                </form>
                            </div>
                            <div className="modal-footer">
                                <div className="pull-left">
                                    <button type="button" className={delete_cancel_class} onClick={delete_cancel_button}>{delete_cancel_text}</button>
                                </div>
                                <button type="button" className="btn btn-primary" onClick={edit_submit_button} >{edit_submit_text}</button>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    });

    // Renders the event detail modal.
    return React.render(
        <EventDetailModal />,
        document.getElementById('event-detail-modal-container')
    );
})(window.React, window.jQuery);