// Represents the react class to be used for the start and end date time pickers
// for use in the event modal.
var DateTimeField = (function(React, $) {
    return React.createClass({

        componentDidMount: function() {
            var start_picker = $(this.refs.startpicker.getDOMNode());
            var end_picker = $(this.refs.endpicker.getDOMNode());

            start_picker.datetimepicker();
            end_picker.datetimepicker();

            // Linking start, end datetime pickers
            start_picker.on("dp.change", function (e) {
                if (e.date)
                    $(this.refs.endpicker.getDOMNode()).data("DateTimePicker").minDate(e.date);
                else
                    $(this.refs.endpicker.getDOMNode()).data("DateTimePicker").minDate(false);
            }.bind(this));
            end_picker.on("dp.change", function (e) {
                if (e.date)
                    $(this.refs.startpicker.getDOMNode()).data("DateTimePicker").maxDate(e.date);
                else
                    $(this.refs.startpicker.getDOMNode()).data("DateTimePicker").maxDate(false);
            }.bind(this));
        },

        // Renders a bootstrap linked date time picker to choose start and end dates.
        render: function() {
           return (
                <div>
                    <div className="form-group">
                        <div className='input-group date' ref="startpicker" id='start-picker'>
                            <input type='text' ref="start" className="form-control" placeholder="Start time" />
                                <span className="input-group-addon">
                                <span className="glyphicon glyphicon-calendar"></span>
                            </span>
                        </div>
                    </div>
                    <div className="form-group">
                        <div className='input-group date' ref="endpicker" id='end-picker'>
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
})(window.React, window.jQuery);