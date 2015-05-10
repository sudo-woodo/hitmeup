(function(React, $, _) {
    'use strict';
    var cx = React.addons.classSet;
  //  var transitionTo = Router.transitionTo;
    var fromServer = [
        {
            image: 'http://i.ytimg.com/vi/82yHd99YxnY/maxresdefault.jpg',
            text: 'FedoraGuy420 has friend requested you!',
            message: 'Hi I am your bestie yooooooooooo',
            time: '4 hours ago',
            read: false,
            action: '/'
        },
        {
            image: 'http://i1.kym-cdn.com/entries/icons/facebook/000/011/121/tumblr_m8t7bxSG2k1r61mz1o5_250.gif',
            text: 'MrSkeltal has friend requested you!',
            message: 'hey you wanna hang out sometime?',
            time: '5 hours ago',
            read: true,
            action: '/notifications'
        },
        {
            image: 'https://www.petfinder.com/wp-content/uploads/2012/11/122163343-conditioning-dog-loud-noises-632x475.jpg',
            text: 'NoNose has friend requested you!',
            message:'I have no nose so you wanna befriend with me?',
            time: '3 days ago',
            read: true,
            action: '/notifications/1'
        },
        {
            image: 'http://i0.kym-cdn.com/entries/icons/original/000/013/564/aP2dv.gif',
            text: 'Wiseman has friend requested you!',
            message: 'wow zoom how pronounce amaze must fast very space',
            time: '500 years ago',
            read: true,
            action: '/notifications/2'
        }
    ];

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
