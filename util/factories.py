from django.db.models.signals import post_save
import factory
from factory.django import DjangoModelFactory
from .util import random_string
from django.conf.urls.static import static
from django.contrib.auth.models import User
from user_accounts.models import UserProfile, create_user_profile
from notifications.models import Notification


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user_%s' % n)
    password = factory.PostGenerationMethodCall('set_password', random_string())
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u)

    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory('util.factories.UserProfileFactory', 'user')

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(create_user_profile, User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_user_profile, User)
        return user


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    # We pass in profile=None to prevent UserFactory from creating another profile
    # (this disables the RelatedFactory)
    user = factory.SubFactory(UserFactory, profile=None)

    phone = '+1234567890'
    bio = factory.LazyAttribute(lambda p: "%s's biography..." % p.user.username)


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserProfileFactory)
    image_url = static('hitmeup/img/hitmeup_square.png')
    action_url = 'https://www.google.com/'
    text = factory.Sequence(lambda n: "Notification %s" % n)
