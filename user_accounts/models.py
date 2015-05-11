import django.dispatch
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from ourcalendar.logic.intervals import Interval
from user_accounts.templatetags import gravatar
from django.utils import timezone


request_friend = django.dispatch.Signal(providing_args=["from_friend", "to_friend"])
accept_friend = django.dispatch.Signal(providing_args=["from_friend", "to_friend"])


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    outgoing_friends = models.ManyToManyField('self', through='Friendship',
                                              symmetrical=False,
                                              related_name='incoming_friends')
    phone_regex = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Phone number must be entered in the format: "
                "'+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=16, validators=[phone_regex], blank=True)
    bio = models.TextField(max_length=300, blank=True)

    def __unicode__(self):
        return self.user.username

    # Word of caution: none of these attributes are "settable."
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    def get_gravatar_url(self, size=80):
        return gravatar.gravatar_url(self.user.email, size)

    # Calendar helpers

    # Intersects your free times with another user's
    def intersect_free(self, other, complement_range):
        """
        Intersects this profile's free times with another profile's.

        :param other: The other profile
        :param range: The complement range Interval
        :return: The complemented list of Intervals
        """
        # Grab valid events
        from ourcalendar.models import Event

        self_events = Event.objects.filter(calendar__ownder=self,
                                           start__gt=complement_range.start,
                                           end__lt=complement_range.end)
        other_events = Event.objects.filter(calendar__ownder=other,
                                            start__gt=complement_range.start,
                                            end__lt=complement_range.end)

        # Flatten into one list
        all_events = Interval.flatten_intervals(
            [e.interval for e in self_events] +
            [e.interval for e in other_events]
        )

        # Return the complement
        return Interval.complement_intervals(all_events, complement_range)

    # Whether or not this user is available right now
    @property
    def is_free(self):
        for event in Event.objects.filter(calendar__owner=self):
            if event.happens_when(timezone.now()):
                return False
        return True

    # Friendship helpers

    @property
    def friends(self):
        # Only friends you have accepted AND friends that have accepted you
        return self.outgoing_friends.filter(
            incoming_friendships__accepted=True) & \
            self.incoming_friends.filter(
            outgoing_friendships__accepted=True)

    @property
    def pending_incoming_friends(self):
        return self.incoming_friends.filter(
            outgoing_friendships__accepted=False)

    @property
    def pending_outgoing_friends(self):
        return self.outgoing_friends.filter(
            incoming_friendships__accepted=False)

    def add_friend(self, other):
        # Check if an incoming friendship exists
        try:
            incoming = Friendship.objects.get(
                from_friend=other, to_friend=self)

        # If no, then create a pending outgoing friendship
        except Friendship.DoesNotExist:
            outgoing, created = Friendship.objects.get_or_create(
                from_friend=self, to_friend=other)
            if created:
                request_friend.send(sender=self.__class__,
                                    from_friend=self, to_friend=other)

        # If yes, accept the incoming friendship
        # and make an accepted outgoing friendship
        else:
            outgoing, created = Friendship.objects.get_or_create(
                from_friend=self, to_friend=other)
            outgoing.accepted = incoming.accepted = True
            outgoing.save()
            incoming.save()
            if created:
                accept_friend.send(sender=self.__class__,
                                   from_friend=self, to_friend=other)

        return outgoing, created

    def del_friend(self, other):
        outgoing_deleted, incoming_deleted = True

        # Delete the outgoing
        try:
            Friendship.objects.get(from_friend=self, to_friend=other).delete()
        except Friendship.DoesNotExist:
            outgoing_deleted = False

        # Delete the incoming
        try:
            Friendship.objects.get(from_friend=other, to_friend=self).delete()
        except Friendship.DoesNotExist:
            incoming_deleted = False

        return outgoing_deleted, incoming_deleted


# Auto-create a UserProfile when creating a User
# https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Friendship(models.Model):
    from_friend = models.ForeignKey(UserProfile,
                                    related_name='outgoing_friendships')
    to_friend = models.ForeignKey(UserProfile,
                                  related_name='incoming_friendships')
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_friend', 'to_friend')

    # Ensure not friending self
    def clean(self):
        if self.from_friend == self.to_friend:
            raise ValidationError("Cannot friend yourself.")
        super(Friendship, self).clean()

    # Override default save to validate
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Friendship, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s --[%s]--> %s' % \
               (self.from_friend, 'o' if self.accepted else 'x', self.to_friend)

