(function($HMU, React, $, _) {
    'use strict';

    var cx = React.addons.classSet;


    var FriendsList = React.createClass({
        render: function() {
            var friendNodes = this.props.friends.map(function (friend) {
                return (
                    <FriendBox friend={friend}/>
                );
            });

            return (
                <div className="friends-list">
                    <div className="container-fluid">
                        <div className="row">
                            {friendNodes}
                        </div>
                    </div>
                </div>
            );
        }
    });

    var FriendInfo = React.createClass({
        render: function() {
            var iClasses = {
                'fa': true,
                'fa-li': true
            };
            iClasses[this.props.icon] = true;

            return (
                <li>
                    <i className={ cx(iClasses) }></i>
                    { this.props.children }
                </li>
            )
        }

    });

    var FriendBox = React.createClass({
        render: function() {
            var infoItems = [
                {
                    icon: this.props.friend.fav ? 'fa-heart' : 'fa-heart-o'
                    ,
                    info: <span className="info">
                        <strong>{this.props.friend.name}</strong>
                    </span>
                },
                {
                    icon: this.props.friend.free ? 'fa-check-circle' : 'fa-clock-o'
                    ,
                    info: <span className={'info ' +
                    (this.props.friend.free ? 'free' : 'busy')
                        }>
                            {this.props.friend.free ? 'Free' : 'Busy'}
                    </span>
                },
                {
                    icon: 'fa-envelope',
                    info: <span className="info">
                            {this.props.friend.email}
                    </span>
                },
                {
                    icon: 'fa-phone',
                    info: <span className="info">
                            {this.props.friend.phone}
                    </span>
                },
                {
                    icon: 'fa-calendar-o',
                    info: <a href="" className="calendar-link info">
                        View my Calendar
                    </a>
                }
            ];

            var infoNodes = infoItems.map(function (item) {
                return (
                    <FriendInfo icon={item.icon}>
                        {item.info}
                    </FriendInfo>
                );
            });

            return (
                <div className="friend-box">
                    <div className="col-xs-12 col-sm-6 col-md-4">
                        <div className="panel panel-default">
                            <div className="friend-info panel-body">
                                <div className="profile-pic-container">
                                    <FriendPic
                                        pic=
                                            {this.props.friend.picture_url}
                                    />
                                </div>

                                <div className=
                                    "profile-info-container overflow-control"
                                >
                                    <ul className="fa-ul">
                                        { infoNodes }
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    });

    var FriendPic = React.createClass({
        render: function() {
            return (
                <img
                    src={ this.props.pic }
                    alt="Picture was not found"
                    className="profile-pic img-circle"
                />
            );
        }
    });

    React.render(
        <FriendsList friends={$HMU.friends}/>,
        document.getElementById('friends-list-container')
    );
})(window.$HMU, window.React, window.jQuery, window._);


