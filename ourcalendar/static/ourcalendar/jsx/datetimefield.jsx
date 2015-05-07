var DateTimeField = React.createClass({

    handleSubmit: function(data)  {


    },

    componentDidMount: function() {
        $('#start-picker').datetimepicker();
        $('#end-picker').datetimepicker();

        // Linking start, end datetime pickers
        $("#start-picker").on("dp.change", function (e) {
            if (e.date)
                $('#end-picker').data("DateTimePicker").minDate(e.date);
            else
                $('#end-picker').data("DateTimePicker").minDate(false);
        });
        $("#end-picker").on("dp.change", function (e) {
            if (e.date)
                $('#start-picker').data("DateTimePicker").maxDate(e.date);
            else
                $('#start-picker').data("DateTimePicker").maxDate(false);
        });

        // Reset min, max dates when event creation modal is dismissed
        $('#create-event-modal').on('hidden.bs.modal', function (e) {
            $('#start-picker').data("DateTimePicker").maxDate(false);
            $('#end-picker').data("DateTimePicker").minDate(false);
        })
    },

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