(function($HMU, React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var Notification = React.createClass({
        render: function() {
            return (
                <a className={cx({
                    'panel': true,
                    'panel-default': true,
                    'notification': true,
                    'read': this.props.data.read
                })} href={this.props.data.action}>
                    <div className="panel-body">
                        <div className="notification-main">
                            <img className="notification-img img-thumbnail"
                                 src={this.props.data.image} />
                            <div className="notification-text">
                                {this.props.data.text}
                            </div>
                            <div className="clearfix"></div>
                        </div>
                        <div className="notification-time">
                            {this.props.data.time}
                        </div>
                    </div>
                </a>
            );
        }
    });

    var NotificationList = React.createClass({
        render: function() {
            var notifications = this.props.notifications.map(function(notif) {
                return <Notification data={notif} />
            });

            if (!notifications.length)
                notifications = (
                    <div className="panel panel-default">
                        <div className="panel-body">
                            <div className="no-notification-text">
                                <em>
                                    No notifications.
                                </em>
                            </div>
                        </div>
                    </div>
                );

            return (
                <div className="container notification-list">
                    {notifications}
                </div>
            );
        }
    });

    React.render(
        <NotificationList notifications={$HMU.notifications} />,
        document.getElementById('notification-list-container')
    );
})(window.$HMU, window.React, window.jQuery, window._);
