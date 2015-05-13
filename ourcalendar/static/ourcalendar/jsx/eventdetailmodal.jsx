var EventDetailModal = React.createClass({

    handleEdit: function()  {
        //On edit, need to render a new form with all of the previous inputs already in place.
    },

    handleDelete: function()  {
        //On delete, need to render a confirmation popup (not sure if necessary yet) and then delete the event.

        $('#eventDetailModal').modal('hide');
    },


    //dummy get initial state for the time being.
    getInitialState: function()  {
        return  {};
    },

    render: function()  {
        return(
            <div id="eventDetailModal" className="modal fade">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <button type="button" className="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h3 className="modal-title">Event Detail</h3>
                            <i className="fa fa-clock-o"></i>&nbsp;&nbsp;<span id="start-time"></span> <span id="end-time"></span>
                        </div>
                        <div className="modal-body">
                            <ul className="fa-ul">
                                <li><i className="fa-li fa fa-map-marker"></i><span id="location"></span></li>
                                <li><i className="fa-li fa fa-calendar"></i><span id="description"></span></li>
                            </ul>
                        </div>
                        <div className="modal-footer">
                            <div className="pull-left">
                                <button type="button" className="btn btn-danger" onClick={this.handleDelete}>Delete Event</button>
                            </div>
                            <button type="button" className="btn btn-primary" onClick={this.handleEdit} >Edit Event</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

//Renders the event detail modal.
var detailReactor = React.render(
    <EventDetailModal />,
    document.getElementById('event-detail-modal-container')
);