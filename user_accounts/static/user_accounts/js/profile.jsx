(function($HMU, React, $, _) {
    'use strict';

    var cx = React.addons.classSet;
    var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;

    var STATE = {
        CLEAN: 0,
        PENDING: 1,
        IS_FRIENDS: 2
    };

    var PROPS = {};

    PROPS[STATE.CLEAN] = function(thiz) {
        return {
            status: STATE.CLEAN,
            iconClasses: 'fa-user-plus',
            buttonClasses: 'friend-button add-friend-button',
            text: ' Add Friend',
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
            status: STATE.PENDING,
            iconClasses: 'fa-remove',
            buttonClasses: 'friend-button pending-button',
            text: null,
            clickHandler: function (e) {
                e.preventDefault();
                $.ajax({
                    url: '/api/friends/' + $HMU.profileId + '/',
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
            status: STATE.IS_FRIENDS,
            iconClasses: 'fa-user-times',
            buttonClasses: 'friend-button remove-button',
            text: ' Remove as friend',
            clickHandler: function(e) {
                e.preventDefault();
                $.ajax({
                    url: '/api/friends/' + $HMU.profileId + '/',
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
                    className={cx({
                        'action-button ': true
                        }) + this.props.buttonClasses
                    }
                    onClick={this.props.clickHandler}
                >
                    <i className={cx({
                        'fa ': true
                        }) + this.props.iconClasses
                    }></i>
                    {this.props.children}
                </div>
            )
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
            var pendingMessage = null;
            if (this.state.status == STATE.PENDING) {
                pendingMessage = (
                    <div className="pending-message">
                        <i className="fa fa-share"></i>
                        <span id="pending-text">
                            <em>Request sent</em>
                        </span>
                    </div>
                );
            }
            return (
                <div className="friend-button-set" key={this.state.buttonClasses}>
                    <ActionButton
                        buttonClasses={this.state.buttonClasses}
                        iconClasses={this.state.iconClasses}
                        clickHandler={this.state.clickHandler}
                        status={this.state.status}
                    >
                        {this.state.text}
                    </ActionButton>
                    { pendingMessage }
                </div>
            );
        }
    });

    if($HMU.showFriendButton) {
        React.render(
            <FriendButton/>,
            document.getElementById('friend-button-container')
        );
    }
})(window.$HMU, window.React, window.jQuery, window._);
