(function($HMU, React, $, _) {
    'use strict';

    var STATE = {
        CLEAN: 0,
        PENDING: 1,
        IS_FRIENDS: 2
    };

    var PROPS = {};
    PROPS[STATE.CLEAN] = function(thiz) {
        return {
            icon: 'fa fa-user-plus',
            button: 'friend-button add-friend-button',
            text: 'Add Friend',
            clickHandler: function (e) {
                e.preventDefault();
                $.ajax({
                    url: '/api/friends/' + $HMU.profileId + '/',
                    method: 'POST',
                    success: function (data) {
                        if(data.accepted) {
                            thiz.setState(PROPS[STATE.IS_FRIENDS](thiz));
                        }
                        else {
                            thiz.setState(PROPS[STATE.PENDING](thiz));
                        }

                    },
                    error: function (data) {
                        alert('Something went wrong, please try again.');
                    }
                });
            }
        }
    };
    PROPS[STATE.PENDING] = function(thiz) {
        return {
            icon: 'fa fa-pulse fa-spinner',
            button: 'friend-button pending-button',
            text: 'Friend Request sent (Click to cancel)',
            clickHandler: function (e) {
                e.preventDefault();
                $.ajax({
                    url: '/api/friends/' + $HMU.profileId,
                    method: 'DELETE',
                    success: function (data) {
                        thiz.setState(PROPS[STATE.CLEAN](thiz));
                    },
                    error: function (data) {
                        alert('Something went wrong, please try again2.');
                    }
                });
            }
        }
    };
    PROPS[STATE.IS_FRIENDS] = function(thiz) {
        return {
            icon: 'fa fa-user-times',
            button: 'friend-button remove-button',
            text: 'Remove as friend',
            clickHandler: function(e) {
                e.preventDefault();
                $.ajax({
                    url: '/api/friends/' + $HMU.profileId,
                    method: 'DELETE',
                    success: function(data) {
                        thiz.setState(PROPS[STATE.CLEAN](thiz));
                    },
                    error: function(data) {
                        alert('Something went wrong, please try again2.');
                    }
                });
            }
        }
    };

    var ActionButton = React.createClass({
         render: function() {
             return (
                 <div
                     id="friend-button"
                     className={this.props.button}
                     onClick={this.props.clickHandler}
                 >
                     <i className={this.props.icon}></i>
                     <span id="friend-button-text">
                         {this.props.children}
                     </span>
                 </div>
             );
         }
    });

    var FriendButton = React.createClass({
        getInitialState: function() {
            switch($HMU.status) {
                case STATE.CLEAN:
                    return PROPS[STATE.CLEAN](this);

                case STATE.PENDING:
                    return PROPS[STATE.PENDING](this);

                case STATE.IS_FRIENDS:
                    return PROPS[STATE.IS_FRIENDS](this);
            }
        },

        render: function() {
            return (
                <ActionButton
                    button={this.state.button}
                    icon={this.state.icon}
                    clickHandler={this.state.clickHandler}
                >
                    {this.state.text}
                </ActionButton>
            );
         }
    });

    if($HMU.showFriendButton) {
        React.render(
            <FriendButton/>,
            document.getElementById('button-container')
        );
    }
})(window.$HMU, window.React, window.jQuery, window._);
