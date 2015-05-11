import django.dispatch
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from user_accounts.templatetags import gravatar


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
    def username(self):
        return self.user.username

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

    @property
    def basic_serialized(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'picture_url': self.get_gravatar_url(size=100)
        }

    # Throws IntegrityError if friendship already exists
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
    favorite = models.BooleanField(default=False)

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

