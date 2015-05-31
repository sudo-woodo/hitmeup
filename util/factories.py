from django.db.models.signals import post_save
from django.templatetags.static import static
from django.utils.crypto import get_random_string
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from communications.models import Subscription, create_subscription
from ourcalendar.models import Event, Calendar, create_calendar
from user_accounts.models import UserProfile, create_user_profile
from notifications.models import Notification


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user_%s' % n)
    password = factory.PostGenerationMethodCall('set_password', get_random_string())
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)

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

    calendar = factory.RelatedFactory('util.factories.CalendarFactory', 'owner')
    subscription = factory.RelatedFactory('util.factories.SubscriptionFactory', 'profile')

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(create_calendar, UserProfile)
        post_save.disconnect(create_subscription, UserProfile)

        user = super(UserProfileFactory, cls)._generate(create, attrs)

        post_save.connect(create_calendar, UserProfile)
        post_save.connect(create_subscription, UserProfile)

        return user

class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription

    profile = factory.SubFactory(UserProfileFactory, subscription=None)


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserProfileFactory)
    image_url = static('hitmeup/img/hitmeup_square.png')
    action_url = 'https://www.google.com/'
    text = factory.Sequence(lambda n: "Notification %s" % n)


class CalendarFactory(DjangoModelFactory):
    class Meta:
        model = Calendar

    owner = factory.SubFactory(UserProfileFactory, calendar=None)
    title = "Default"
    color = "#267F00"


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    calendar = factory.SubFactory(CalendarFactory)
    title = factory.Sequence(lambda n: "Ethan's Sweet %s" % n)
    location = factory.Sequence(lambda n: "Sweet %s Club" % n)
    description = factory.Sequence(lambda n: "Ethan is turning %s, "
                                             "so let's turn up!" % n)
