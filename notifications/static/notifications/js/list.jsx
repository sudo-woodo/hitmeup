(function(React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var fromServer = [
        {
            image: 'http://i.ytimg.com/vi/82yHd99YxnY/maxresdefault.jpg',
            text: 'FedoraGuy420 has friend requested you!',
            time: '4 hours ago',
            read: false,
            action: '/'
        },
        {
            image: 'http://i1.kym-cdn.com/entries/icons/facebook/000/011/121/tumblr_m8t7bxSG2k1r61mz1o5_250.gif',
            text: 'MrSkeltal has friend requested you!',
            time: '5 hours ago',
            read: true,
            action: '/notifications'
        }
    ];

    var Notification = React.createClass({
        render: function() {
            console.log('hi');
            return (
                <div className={cx({
                        'panel': true,
                        'panel-default': true,
                        'notification': true,
                        'read': this.props.data.read
                    })}>
                    <div className="panel-body">
                        <img className="notification-img" src={this.props.data.image} />
                        <div className="notification-text">
                            {this.props.data.text}
                        </div>
                        <div className="notification-time">
                            {this.props.data.time}
                        </div>
                    </div>
                </div>
            );
        }
    });

    var NotificationList = React.createClass({
        getInitialState: function() {
            return {notifications: []};
        },
        componentDidMount: function() {
            this.setState({
                notifications: fromServer
            });
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
})(window.React, window.jQuery, window._);