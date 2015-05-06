var DateTimeField = React.createClass({

    handleSubmit: function(data)  {


    },

    componentDidMount: function() {
        console.log('a');
        $('#datetimepicker6').datetimepicker();
        $('#datetimepicker7').datetimepicker();
        $("#datetimepicker6").on("dp.change", function (e) {
            $('#datetimepicker7').data("DateTimePicker").minDate(e.date);
        });
        $("#datetimepicker7").on("dp.change", function (e) {
            $('#datetimepicker6').data("DateTimePicker").maxDate(e.date);
        });
    },

    render: function() {
       return (
            <div>
                <div className="form-group">
                    <div className='input-group date' id='datetimepicker6'>
                        <input type='text' className="form-control" />
                            <span className="input-group-addon">
                            <span className="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
                <div className="form-group">
                    <div className='input-group date' id='datetimepicker7'>
                        <input type='text' className="form-control" />
                        <span className="input-group-addon">
                            <span className="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
            </div>
       );
   }
});