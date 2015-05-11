# See dynamic_components.context_processors for format
entries = [
    {
        'name': 'Home',
        'view': 'static_pages:home',
        'auth_required': False
    },
    {
        'name': 'Friends',
        'view': 'user_accounts:friendsList',
        'auth_required': True
    }
]