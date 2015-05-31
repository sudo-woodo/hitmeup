var RepeatBox = (function(React, $)  {

    return React.createClass({

        componentDidMount: function()  {
            $('.selectpicker').selectpicker();
            $('#end_repeat_picker').datetimepicker({
                format: 'MM/DD/YYYY'
            });

            // Set the day on the selectpicker to whatever day of the week user selected.
            var date = $('#start-picker').data("DateTimePicker").date();
            var days_picker = $('#days');

            // Because we have sunday at end.
            var date_val = moment(date).weekday()-1;
            if ( date_val === -1 )  {
                date_val = 6;
            }
            days_picker.selectpicker('val', date_val);
            days_picker.selectpicker('render');
        },

        // Render necessary repeat information.
        render: function()  {
            // Would have been used to customly render an input form if user selects custom.
            // TODO add below to bottom of first selectpicker to allow for custom frequency. Need to dynamically get value of selectpicker.
            // <option value="-1">Custom</option>
            // TODO make the repeat end date linked with the start and end time (since it will look better)

            return (
                <div>
                    <p>
                        <select className="selectpicker" id="frequency" multiple title="Every week" data-width="49%" data-max-options="1">
                            <option value="1">Every week</option>
                            <option value="2">Every 2 weeks</option>
                            <option value="3">Every 3 weeks</option>
                            <option value="4">Every 4 weeks</option>
                            <option value="5">Every 5 weeks</option>
                            <option value="8">Every 8 weeks</option>
                            <option value="52">Every 52 weeks</option>
                        </select>
                        <select className="selectpicker days-picker" id="days" multiple title="Select days" data-width="49%" ref="days">
                            <option value="6">Sunday</option>
                            <option value="0">Monday</option>
                            <option value="1">Tuesday</option>
                            <option value="2">Wednesday</option>
                            <option value="3">Thursday</option>
                            <option value="4">Friday</option>
                            <option value="5">Saturday</option>
                    </select>
                    </p>
                    <div className="form-group">
                        <div className='input-group date' id='end_repeat_picker'>
                            <input type='text' placeholder="End repeat on" ref="endDate" className="form-control" />
                            <span className="input-group-addon">
                                <span className="glyphicon glyphicon-calendar">
                                </span>
                            </span>
                        </div>
                    </div>
                </div>
            );
        }
    });

})(window.React, window.jQuery);