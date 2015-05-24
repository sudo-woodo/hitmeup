(function($HMU, React, $, _) {
    'use strict';

    var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;
    var cx = React.addons.classSet;

    var FriendsList = React.createClass({
        refreshHandler: function(e) {
            e.preventDefault();
            $.ajax({
                url: '/api/friends/',
                method: 'GET',
                success: function(data) {
                    this.setState({friends: data['objects']});
                }.bind(this),
                error: function() {
                    alert('Something went wrong with retrieving your ' +
                    'friends list, please try refreshing the page.')
                }
            });
        },

        getInitialState: function() {
            return {friends: this.props.friends};
        },


        render: function() {
            var favorites = [];
            var regulars = [];
            this.state.friends.forEach(function(friend) {
                var friendNode = <FriendBox friend={friend} key={friend.username}/>;
                if(friend.favorite) {
                    favorites.push(friendNode);
                } else {
                    regulars.push(friendNode);
                }
            });
            return (
                <div className="friends-list">
                    <div className="container-fluid">
                        <div className="row">
                            {favorites}
                            {regulars}
                        </div>
                        <div
                            className="btn btn-lg btn-default refresh-button"
                            onClick={this.refreshHandler}
                        >
                            <i className="fa fa-refresh refresh-icon"></i>
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
                    <i
                        className={ cx(iClasses) }
                        onClick={this.props.clickHandler}
                    ></i>
                    { this.props.children }
                </li>
            )
        }

    });

    var FriendBox = React.createClass({
        favHandler: function(e) {
            e.preventDefault();
            $.ajax({
                url: '/api/friends/' + this.props.friend.id + '/',
                method: 'PUT',
                data: JSON.stringify({favorite: !this.state.friend.favorite}),
                success: function(data) {
                    this.setState({friend: data});
                }.bind(this),
                error: function() {
                    alert('Something went wrong with favoriting the friend,' +
                    ' please try again.');
                }
            });
        },

        getInitialState: function () {
            return {friend: this.props.friend}
        },

        render: function() {
            var infoItems = [
                {
                    icon: (this.state.friend.favorite ? 'fa-heart fav' : 'fa-heart-o') +
                        ' fav-icon'
                    ,
                    info: <span className="info">
                        <strong>{this.props.friend.username}</strong>
                    </span>,
                    clickHandler: this.favHandler
                },
                {
                    icon: this.props.friend.free ?
                        'fa-check-circle free-icon' : 'fa-clock-o busy-icon'
                    ,
                    info: <span className={
                        'info ' +
                        (this.props.friend.free ? 'free' : 'busy')
                    }>
                            {this.props.friend.free ? 'Free' : 'Busy'}
                    </span>,
                    clickHandler: null
                },
                {
                    icon: 'fa-envelope',
                    info: <a
                        href={
                            this.props.friend.email ?
                            'mailto:' + this.props.friend.email :
                            '#'
                        }
                        className="info"
                    >
                            {this.props.friend.email}
                    </a>,
                    clickHandler: null
                },
                {
                    icon: 'fa-phone',
                    info: <a
                        href={
                            this.props.friend.phone ?
                            'tel:' + this.props.friend.phone :
                            '#'
                        }
                        className="info"
                    >
                            {this.props.friend.phone || '—'}
                    </a>,
                    clickHandler: null
                },
                {
                    icon: 'fa-user',
                    info: <a
                        href={this.props.friend.profile_url}
                        className="profile-link info"
                    >
                        My Profile
                    </a>,
                    clickHandler: null
                }
            ];

            var infoNodes = infoItems.map(function (item) {
                return (
                    <FriendInfo
                        icon={item.icon}
                        clickHandler={item.clickHandler}
                    >
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
                                        pic={this.props.friend.gravatar_url}
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
                    alt="Profile Picture"
                    className="profile-pic img-thumbnail"
                />
            );
        }
    });

    React.render(
        <FriendsList friends={$HMU.friends}/>,
        document.getElementById('friends-list-container')
    );
})(window.$HMU, window.React, window.jQuery, window._);


