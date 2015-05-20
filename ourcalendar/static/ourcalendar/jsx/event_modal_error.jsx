// Class for the error messages when creating or editing events.
// Simply displays the error messages to the user.
var EventModalError = (function(React, $) {
    return React.createClass({
        render: function()  {
            return (
                <div className="alert alert-danger" role="alert">{this.props.children}</div>
            );
        }
    });
})(window.React, window.jQuery);