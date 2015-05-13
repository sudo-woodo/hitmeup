//Represents the react class to be used for the start and end date time pickers
//for use in the event modal.
var DateTimeField = React.createClass({

    componentDidMount: function() {
        var start_picker = $('#start-picker');
        var end_picker = $('#end-picker');

        start_picker.datetimepicker();
        end_picker.datetimepicker();

        // Linking start, end datetime pickers
        start_picker.on("dp.change", function (e) {
            if (e.date)
                $('#end-picker').data("DateTimePicker").minDate(e.date);
            else
                $('#end-picker').data("DateTimePicker").minDate(false);
        });
        end_picker.on("dp.change", function (e) {
            if (e.date)
                $('#start-picker').data("DateTimePicker").maxDate(e.date);
            else
                $('#start-picker').data("DateTimePicker").maxDate(false);
        });
    },

    //renders a bootstrap linked date time picker to choose start and end dates.
    render: function() {
       return (
            <div>
                <div className="form-group">
                    <div className='input-group date' id='start-picker'>
                        <input type='text' ref="start" className="form-control" placeholder="Start time" />
                            <span className="input-group-addon">
                            <span className="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
                <div className="form-group">
                    <div className='input-group date' id='end-picker'>
                        <input type='text' ref="end" className="form-control" placeholder="End time" />
                        <span className="input-group-addon">
                            <span className="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
            </div>
       );
   }
});