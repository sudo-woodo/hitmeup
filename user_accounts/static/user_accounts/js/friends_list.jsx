(function(React, $, _) {
    'use strict';

    var cx = React.addons.classSet;

    /*$(document).on('mouseenter', ".info", function () {
     var $this = $(this);
     if (this.width < this.scrollWidth) {
         $this.tooltip({
             title: $this.text(),
             placement: "bottom"
         });
         $this.tooltip('show');
     }
    });*/

    var data = [
        {
            'name': 'Gary Gillespie',
            'picture_url': 'https://media.licdn.com/mpr/mpr/shrink_200_200/p/2/000/0db/205/1492be8.jpg',
            'free': true,
            'email': 'coconutwaterlvr@hotmail.com',
            'phone': '800-124-1457',
            'fav': true
        },
        {
            'name': 'RickyOrd',
            'picture_url': 'http://cseweb.ucsd.edu/~ricko/images/Rick-Headshot.jpg',
            'free': false,
            'email': 'CAFEBABE@msn.com',
            'phone': '812-463-7334',
            'fav': true
        },
        {
            'name': 'Massimiliano "MAX" Menarini',
            'picture_url':
                'https://sosa.ucsd.edu/confluence/download/attachments/1212424/mmenarini_tn.jpg?version=1&modificationDate=1255626677000',
            'free': false,
            'email': 'agile@aim.net',
            'phone': '134-643-8754',
            'fav': false
        },
        {
            'name': 'Papa Phil',
            'picture_url':
                'http://users.sdsc.edu/~phil/images/phil.jpg',
            'free': false,
            'email': 'vimenthusiast@yahoo.com',
            'phone': '942-325-2678',
            'fav': true
        },
        {
            'name': 'Barack Obama',
            'picture_url':
                'http://api.ning.com/files/2R8JQXTOEkNOw74rkMxAns-rsBoRXm3osCtTiAzhQXMv5rjfjMHGEW6oTxHBdSrHBCb1Y2T20Yjmnx0ZjS*EYsk1msNWH-9f/ObamaFunnyFace.jpg',
            'free': true,
            'email': 'change@whitehouse.gov',
            'phone': '321-542-YUME',
            'fav': false
        },
        {
            'name': 'Snoop Dogg',
            'picture_url':
                'http://assets.rollingstone.com/assets/images/story/snoop-dogg-talks-holograms-2pac-and-chronic-in-web-chat-20130509/snoop-624-1368121236.jpg',
            'free': false,
            'email': 'snoop@sdsu.edu',
            'phone': '568-234-3800',
            'fav': false
        },
        {
            'name': 'Phreak',
            'picture_url':
                'http://i.ytimg.com/vi/RAIq5V6LqPM/maxresdefault.jpg',
            'free': true,
            'email': 'tonsofdamage@gmail.com',
            'phone': '123-855-8933',
            'fav': false
        },
        {
            'name': 'Joseph Joestar',
            'picture_url':
                'http://www.learnspanishtoday.com/img/businessman.jpg',
            'free': false,
            'email': 'hamon@gmail.com',
            'phone': '847-664-8436',
            'fav': true
        }
    ];

    var FriendsList = React.createClass({
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
                    icon:
                        this.props.friend.fav ? 'fa-heart' : 'fa-heart-o'
                    ,
                    info:
                        <span className="info">
                            <strong>{this.props.friend.name}</strong>
                        </span>
                },
                {
                    icon:
                        this.props.friend.free ? 'fa-check-circle' : 'fa-clock-o'
                    ,
                    info:
                        <span className={'info ' +
                            (this.props.friend.free ? 'free' : 'busy')
                        }>
                            {this.props.friend.free ? 'Free' : 'Busy'}
                        </span>
                },
                {
                    icon: 'fa-envelope',
                    info:
                        <span className="info">
                            {this.props.friend.email}
                        </span>
                },
                {
                    icon: 'fa-phone',
                    info:
                        <span className="info">
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

            var infoNodes = infoItems.map(function(item) {
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
                                <div className="profile-info-container">
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
        <FriendsList data={data}/>,
        document.getElementById('friends-list-container')
    );
})(window.React, window.jQuery, window._);


