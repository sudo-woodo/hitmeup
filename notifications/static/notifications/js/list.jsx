(function(React, $, _) {
    'use strict';
    var cx = React.addons.classSet;
  //  var transitionTo = Router.transitionTo;
    var fromServer = [];

    var Notification = React.createClass({
        handleClick: function(e){
            console.log("Clicked");
            e.preventDefault();
            // js redirect
            window.location.href = this.props.data.action;
        },

        render: function() {
            console.log('hi');
            return (
                <div className={cx({
                    'panel': true,
                    'panel-default': true,
                    'notification': true,
                    'read': this.props.data.read
                })}>
                  <div className="panel-body" onClick={this.handleClick} >
                        <img className="notification-img" src={this.props.data.image} />
                         <div className="body-container" >
                             <div className="notification-text">
                                {this.props.data.text}
                             </div>
                             <div className="notification-time">
                                {this.props.data.time}
                             </div>
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
            setInterval(this.loadCommentsFromServer, this.props.pollInterval);
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
