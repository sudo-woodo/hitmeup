(function(React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var FriendButton = React.createClass({
        render: function() {
            return (
                 <a href="" id="friend-button">
                    <i className="fa fa-user-plus"></i>
                    <span id="add-friend-text">
                        Add as Friend
                    </span>
                </a>
             );
         }
     });

    React.render(
        <FriendButton/>,
        document.getElementById('button-container')
    );
})(window.React, window.jQuery, window._);
