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

                $(this.refs.inputForm.refs.datetime.refs.startpicker.getDOMNode()).data("DateTimePicker").date(moment(this.state.start));
                $(this.refs.inputForm.refs.datetime.refs.endpicker.getDOMNode()).data("DateTimePicker").date(moment(this.state.end));
            }

        },

        handleEdit: function()  {
            // TODO On edit, need to render a new form with all of the previous inputs already in place.
            this.setState({edit: true});


        },

        handleDelete: function()  {
            // TODO On delete and then delete the event.


            $('#eventDetailModal').modal('hide');
        },

        handleSubmit: function()  {
            // TODO actually do this
            var putData = {
                title: React.findDOMNode(this.refs.inputForm.refs.title).value.trim(),
                start: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.start).value.trim(),
                end: React.findDOMNode(this.refs.inputForm.refs.datetime.refs.end).value.trim(),
                location: React.findDOMNode(this.refs.inputForm.refs.location).value.trim(),
                description: React.findDOMNode(this.refs.inputForm.refs.description).value.trim(),
                calendar: 'Default'      // Necessary for AJAX request
            };

            // Will need to do error checking in the future. Copy format of create_event_modal.

            var startMoment = moment(putData.start);
            var endMoment = moment(putData.end);

            putData.start = moment(putData.start).format('YYYY-MM-DD HH:mm');
            putData.end = moment(putData.end).format('YYYY-MM-DD HH:mm');

            // AJAX request to edit the event
            $.ajax({
                url: '/api/events/' + this.state.id + '/',
                type: "PUT",
                data: JSON.stringify(putData),
                contentType: "application/json",
                success: function(response) {},
                complete: function() {},
                error: function (xhr, textStatus, thrownError) {
                    // TODO handle error case?
                    console.log(xhr.responseText);
                }
            });

            var result = $('#calendar').fullCalendar('clientEvents', this.state.id )[0];
            result.title = putData.title;
            result.start = startMoment;
            result.end = endMoment;
            result.description = putData.description;
            result.location = putData.location;

            $('#calendar').fullCalendar('updateEvent', result);
            $('#eventDetailModal').modal('hide');
        },

        handleCancel: function()  {
            this.setState({edit: false});
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
                id: -1
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
            var form = this.state.edit ? <InputForm ref="inputForm" /> : <DefaultDetail location={this.state.location} description={this.state.description} />;
            var edit_submit_button = this.state.edit ? this.handleSubmit : this.handleEdit;
            var edit_submit_text = this.state.edit ? "Save Changes" : "Edit Event";
            var delete_cancel_button = this.state.edit ? this.handleCancel : this.handleDelete;
            var delete_cancel_text = this.state.edit ? "Cancel" : "Delete";
            var delete_cancel_class = this.state.edit ? "btn btn-primary" : "btn btn-danger";

            return(
                <div id="eventDetailModal" className="modal fade">
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                <h3 className="modal-title">{this.state.title}</h3>
                                <i className="fa fa-clock-o"></i>&nbsp;&nbsp;<span id="start-time">{this.state.start}</span> &mdash; <span id="end-time">{this.state.end}</span>
                            </div>
                            <div className="modal-body">
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