(function($HMU, React, $, _) {
    'use strict';

    var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;

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
                        if(data.accepted)
                            thiz.setState(PROPS[STATE.IS_FRIENDS](thiz));
                        else
                            thiz.setState(PROPS[STATE.PENDING](thiz));
                    },
                    error: function () {
                        alert('Something went wrong with the friend request,' +
                        ' please try again.');
                    }
                });
            }
        }
    };

    PROPS[STATE.PENDING] = function(thiz) {
        return {
            icon: 'fa fa-pulse fa-spinner',
            button: 'friend-button pending-button',
            text: 'Friend request sent (click to cancel)',
            clickHandler: function (e) {
                e.preventDefault();
                $.ajax({
                    url: '/api/friends/' + $HMU.profileId,
                    method: 'DELETE',
                    success: function () {
                        thiz.setState(PROPS[STATE.CLEAN](thiz));
                    },
                    error: function () {
                        alert('Something went wrong with cancelling the friend ' +
                        'request, please try again.');
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
                    success: function() {
                        thiz.setState(PROPS[STATE.CLEAN](thiz));
                    },
                    error: function() {
                        alert('Something went wrong with removing the friend,' +
                        ' please try again.');
                    }
                });
            }
        }
    };

    var ActionButton = React.createClass({
         render: function() {
             return (
                 <div
                     key={this.props.button}
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
                    break;

                case STATE.PENDING:
                    return PROPS[STATE.PENDING](this);
                    break;

                case STATE.IS_FRIENDS:
                    return PROPS[STATE.IS_FRIENDS](this);
                    break;
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