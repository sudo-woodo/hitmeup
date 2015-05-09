(function(React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    var FriendButton = React.createClass({
        render: function() {
            var friendNodes = this.props.data.map(function (friend) {
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

    React.render(
        <FriendsList data={data}/>,
        document.getElementById('friends-list-container')
    );
})(window.React, window.jQuery, window._);
