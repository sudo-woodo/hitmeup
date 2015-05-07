import factory
from .util import random_string
from django.contrib.auth.models import User
from notifications.models import Notification

UserFactory = factory.make_factory(User,
    username=factory.LazyAttribute(lambda _: random_string()),
    password=factory.PostGenerationMethodCall('set_password', random_string()),
    email=factory.LazyAttribute(lambda u: '%s@example.com' % u.username),
)

NotificationFactory = factory.make_factory(Notification,
    username=factory.LazyAttribute(lambda _: random_string()),
    password=factory.PostGenerationMethodCall('set_password', random_string()),
    email=factory.LazyAttribute(lambda u: '%s@example.com' % u.username),
)