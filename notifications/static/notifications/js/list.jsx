(function($HMU, React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var Notification = React.createClass({
        handleClick: function(e){
            e.preventDefault();

            // js redirect
            window.location.href = this.props.data.action;
        },

        render: function() {
            return (
                <div className={cx({
                    'panel': true,
                    'panel-default': true,
                    'notification': true,
                    'read': this.props.data.read
                })}>
                    <div className="panel-body" onClick={this.handleClick} >
                        <img className="notification-img img-thumbnail"
                             src={this.props.data.image} />
                        <span className="notification-text">
                            {this.props.data.text}
                        </span>
                        <br />
                        <span className="notification-time">
                            {this.props.data.time}
                        </span>
                    </div>
                </div>
            );
        }
    });

    var NotificationList = React.createClass({
        getInitialState: function() {
            return {notifications: $HMU.notifications};
        },

        render: function() {
            var notifications = this.state.notifications.map(function(notif) {
                return <Notification data={notif} />
            });

            return (
                <div className="container notification-list">
                    {notifications}
                </div>
            );
        }
    });

    React.render(
        <NotificationList />,
        document.getElementById('notification-list-container')
    );
})(window.$HMU, window.React, window.jQuery, window._);
