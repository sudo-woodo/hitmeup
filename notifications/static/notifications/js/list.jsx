(function($HMU, React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var Notification = React.createClass({
        render: function() {
            return (
                <div className="col-xs-12 col-md-6">
                    <a className={cx({
                        'panel': true,
                        'panel-default': true,
                        'notification': true,
                        'read': this.props.data.read
                    })} href={this.props.data.action}>
                        <div className="panel-body">
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
                    </a>
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
                    <div className="row">
                        {notifications}
                    </div>
                </div>
            );
        }
    });

    React.render(
        <NotificationList />,
        document.getElementById('notification-list-container')
    );
})(window.$HMU, window.React, window.jQuery, window._);
