var EventDetailModal = React.createClass({

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
                    </div>
                </div>
            </div>
        );
    }
});

//Renders the event detail modal.
var reactor = React.render(
    <EventDetailModal />,
    document.getElementById('event-detail-modal-container')
);