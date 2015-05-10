(function($HMU, React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var STATE = {
        CLEAN: 0,
        PENDING: 1,
        IS_FRIENDS: 2
    };

    var PROPS = {};
    PROPS[STATE.CLEAN] = {
        icon: 'fa fa-user-plus',
        button: 'add-friend-button',
        status: STATE.CLEAN,
        clickHandler: this.addFriendHandler
    };
    PROPS[STATE.PENDING] = {
        icon: 'fa fa-spin fa-spinner',
        button: 'pending-button',
        status: STATE.PENDING
    };
    PROPS[STATE.IS_FRIENDS] = {
        icon: 'fa fa-user-times',
        button: 'remove-button',
        status: STATE.IS_FRIENDS,
        clickHandler: this.removeFriendHandler
    };

    var FriendButton = React.createClass({
        getInitialState: function() {
            if ($HMU.status == STATE.CLEAN) {
                return PROPS[STATE.CLEAN]
            }
            if ($HMU.status == STATE.PENDING) {
                return PROPS[STATE.PENDING]
            }
            if ($HMU.status == STATE.IS_FRIENDS) {
                return PROPS[STATE.IS_FRIENDS]
            }
        },

        addFriendHandler: function(e) {
            e.preventDefault();
            $.ajax({
                url: '/api/friends/' + $HMU.profile_id,
                method: 'POST',
                success: function(data) {
                    if(data.accepted) {
                        this.setState(PROPS[STATE.IS_FRIENDS]);
                    }

                    else {
                        this.setState(PROPS[STATE.PENDING])
                    }
                },
                error: function(data) {
                    this.setState(PROPS[STATE.CLEAN])
                }
            });
        },

        removeFriendHandler: function(e) {
            e.preventDefault();

        },
        componentDidMount: function() {
            $.ajax({
                url: '/api/friends/' + $HMU.profile_id,
                method: 'GET',
                success: function(data) {
                    if(data.accepted) {
                        this.setState(PROPS[STATE.IS_FRIENDS]);
                    }

                    else {
                        this.setState(PROPS[STATE.PENDING])
                    }
                },
                error: function(data) {
                    this.setState(PROPS[STATE.CLEAN])
                }
            });
        },

        render: function() {
            return (
                <ActionButton
                    buttonClasses={this.state.button}
                    iconClasses={this.state.icon}
                    clickHandler={this.state.clickHandler}
                >
                    {this.state.text}
                </ActionButton>
            )
         }
    });

    var ActionButton = React.createClass({
         render: function() {
             return (
                 <a href="#" id="friend-button" class={this.props.button} onClick={this.props.clickHandler}>
                    <i className={this.props.icon}></i>
                    <span id="friend-button-text">
                        {this.props.children}
                    </span>
                </a>
             )
         }


    });

    React.render(
        <FriendButton/>,
        document.getElementById('button-container')
    );
})(window.$HMU, window.React, window.jQuery, window._);
