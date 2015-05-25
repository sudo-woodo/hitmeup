# See dynamic_components.context_processors for format
entries = [
    {
        'name': 'Home',
        'view': 'static_pages:home',
        'auth_required': False
    },
    {
        'name': 'Friends',
        'view': 'user_accounts:friends_list',
        'auth_required': True
    },
    {
        'name': 'Calendar',
        'view': 'calendar:view_calendar',
        'auth_required': True,
    },
]
