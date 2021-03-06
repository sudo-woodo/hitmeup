(function($HMU, React, $, _) {
    'use strict';

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

            // No friends?
            var mainContent;
            if (!this.state.friends.length)
                mainContent = (
                    <div className="container">
                        <div className="panel panel-default">
                            <div className="panel-body no-friends-panel">
                                <em>
                                    No friends - go add some by searching for them!
                                </em>
                            </div>
                        </div>
                    </div>
                );
            else
                mainContent = (
                    <div className="container">
                        <div className="row">
                            {favorites}
                            {regulars}
                        </div>
                    </div>
                );

            return (
                <div className="friends-list">
                    {mainContent}
                    <div
                        className="btn btn-lg btn-default refresh-button"
                        onClick={this.refreshHandler}
                    >
                        <i className="fa fa-refresh refresh-icon"></i>
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
            );
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
                    icon: (this.state.friend.favorite ?
                            'fa-heart fav' :
                            'fa-heart-o'
                    ) + ' fav-icon',
                    info: (
                        <span className="info">
                            <strong>
                                {this.props.friend.username}
                                {this.props.friend.full_name ?
                                 ' (' + this.props.friend.full_name + ')' : ''}
                            </strong>
                        </span>
                    ),
                    clickHandler: this.favHandler
                },
                {
                    icon: this.props.friend.is_free ?
                        'fa-check-circle free-icon' :
                        'fa-clock-o busy-icon',
                    info: (
                        <span className={
                            'info ' +
                            (this.props.friend.is_free ? 'free' : 'busy')
                        }>
                            {this.props.friend.is_free ? 'Free' : 'Busy'}
                        </span>
                    ),
                    clickHandler: null
                },
                {
                    icon: 'fa-envelope',
                    info: (
                        <a
                            href={
                                this.props.friend.email ?
                                'mailto:' + this.props.friend.email :
                                '#'
                            }
                            className="info"
                        >
                            {this.props.friend.email}
                        </a>
                    ),
                    clickHandler: null
                },
                {
                    icon: 'fa-phone',
                    info: (
                        <a
                            href={
                                this.props.friend.phone ?
                                'tel:' + this.props.friend.phone :
                                '#'
                            }
                            className="info"
                        >
                            {this.props.friend.phone || '—'}
                        </a>
                    ),
                    clickHandler: null
                },
                {
                    icon: 'fa-user',
                    info: (
                        <a
                            href={this.props.friend.profile_url}
                            className="info"
                        >
                            My Profile
                        </a>
                    ),
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
                                    <ul className="fa-ul info-container">
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
                    alt="Profile picture"
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


