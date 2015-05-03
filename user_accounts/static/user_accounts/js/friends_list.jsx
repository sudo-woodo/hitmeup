(function(React, $, _) {
    var cx = React.addons.classSet;
    var data = [
        {
            'name': 'Ethan Ochinchin Chan',
            'picture_url': 'http://i.ytimg.com/vi/90EAmumpAME/maxresdefault.jpg',
            'free': true,
            'email': 'ochinchin@daisuke.edu',
            'phone': '800-124-1457',
            'fav': true
        },
        {
            'name': 'RichardtheGuy',
            'picture_url': 'http://i.ytimg.com/vi/82yHd99YxnY/maxresdefault.jpg',
            'free': false,
            'email': 'euphoira@athiesm.gov',
            'phone': '812-463-7334',
            'fav': true
        },
        {
            'name': 'xXl33t_420_noscopXx',
            'picture_url':
                'https://pbs.twimg.com/profile_images/1550541334/' +
                'eye_reasonably_small_400x400.jpg',
            'free': false,
            'email': '360@getrekt.biz',
            'phone': '134-643-8754',
            'fav': false
        },
        {
            'name': 'kevinChan',
            'picture_url':
                'http://i.telegraph.co.uk/multimedia/archive/02701/' +
                'kim_2701423b.jpg',
            'free': false,
            'email': 'supremeleader@northkorea.northkorea',
            'phone': '942-325-2678',
            'fav': true
        },
        {
            'name': 'BreastBobFin',
            'picture_url':
                'http://images.gmanews.tv/v3/webpics/v3/2014/07/' +
                '2014_07_01_12_49_56.jpg',
            'free': true,
            'email': 'orewa@yume.da',
            'phone': '321-542-YUME',
            'fav': false
        },
        {
            'name': 'Italiano',
            'picture_url':
                'http://img3.wikia.nocookie.net/__cb20100719141605/logopedia/' +
                'images/9/98/Chef_Boyardee.png',
            'free': false,
            'email': 'agile@iteration.com',
            'phone': '568-234-3800',
            'fav': false
        },
        {
            'name': 'naruto',
            'picture_url':
                'http://fc00.deviantart.net/fs71/i/2011/321/0/1/' +
                'my_naruto_cosplay_by_maverickajo-d4ghfz8.jpg',
            'free': true,
            'email': 'believe@it.org',
            'phone': '123-855-8933',
            'fav': false
        },
        {
            'name': 'Pool',
            'picture_url':
                'http://www.cee1.org/sites/www.cee1.org/files/' +
                'images/SwimmingPool_0.jpg',
            'free': false,
            'email': 'swim@water.nz',
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

    var FriendBox = React.createClass({
        render: function() {
            var friendName = {
                name: this.props.friend.name,
                fav: this.props.friend.fav
            };
            return (
                <div className="friend-box">
                    <div className="col-xs-12 col-sm-6 col-md-4">
                        <div className="panel panel-default">
                            <div className="friend-info panel-body">
                                <div className="profile-pic-container">
                                    <FriendPic
                                        friendPic=
                                            {this.props.friend.picture_url}
                                    />
                                </div>
                                <div className="profile-info-container">
                                    <ul className="fa-ul">
                                        <FriendName
                                            friendName={ friendName }
                                        />

                                        <FriendFree
                                            friendFree=
                                                {
                                                    this.props.friend.free
                                                }
                                        />

                                        <FriendEmail
                                            friendEmail=
                                                {
                                                    this.props.friend.email
                                                }
                                        />

                                        <FriendPhone
                                            friendPhone=
                                                {
                                                    this.props.friend.phone
                                                }
                                        />
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
                    src={ this.props.friendPic }
                    alt="test"
                    className="profile-pic img-circle"
                />
            );
        }
    });

    var FriendName = React.createClass({
        render: function() {
            return (
                <li>
                    <i
                        className={cx({
                            'fa': true,
                            'fa-li': true,
                            'fa-heart':
                                this.props.friendName.fav,
                            'fa-heart-o':
                                !this.props.friendName.fav
                        })}
                    ></i>

                    <strong>
                        { this.props.friendName.name }
                    </strong>
                </li>
            );
        }
    });

    var FriendFree = React.createClass({
        render: function() {
            return (
                <li>
                    <i className={cx({
                        'fa': true,
                        'fa-li': true,
                        'fa-check-circle':
                            this.props.friendFree,
                        'fa-clock-o':
                            !this.props.friendFree
                    })}></i>

                    <span className={cx({
                        'free':
                            this.props.friendFree,
                        'busy':
                            !this.props.friendFree
                    })}>
                        {
                            this.props.friendFree
                                ? 'Free'
                                : 'Busy'
                        }
                    </span>


                </li>
            );
        }
    });

    var FriendEmail = React.createClass({
        render: function() {
            return (
                <li>
                    <i className="fa-li fa fa-envelope"></i>
                    { this.props.friendEmail }
                </li>
            );
        }
    });

    var FriendPhone = React.createClass({
        render: function() {
            return (
                <li>
                    <i className="fa-li fa fa-phone"></i>
                    { this.props.friendPhone }
                </li>
            );
        }
    });

    React.render(
        <FriendsList data={data}/>,
        document.getElementById('friends-list')
    );
})(window.React, window.jQuery, window._);


