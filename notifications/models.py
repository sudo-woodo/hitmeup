from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.dispatch.dispatcher import receiver
from user_accounts.models import UserProfile, request_friend, accept_friend
from django.utils import timezone
from communications.emails import send_notification_email


class Notification(models.Model):
    REQUEST_FRIEND = 'request_friend'
    ACCEPT_FRIEND = 'accept_friend'
    NOTIFICATION_STRINGS = {
        REQUEST_FRIEND: '%s has requested to be your friend!',
        ACCEPT_FRIEND: '%s has accepted your friend request!',
    }

    recipient = models.ForeignKey(UserProfile, related_name='notifications')
    image_url = models.CharField(max_length=600)
    action_url = models.CharField(max_length=600)
    text = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return "%s @ %s: %s" % (self.recipient, self.time, self.text)

    @property
    def natural_time(self):
        return naturaltime(self.time)

    @property
    def serialized(self):
        return {
            'image': self.image_url,
            'action': self.action_url,
            'text': self.text,
            'time': self.natural_time,
            'read': self.read,
        }

    def refresh(self):
        # Marks as unread and updates the time
        self.read = False
        self.time = timezone.now()
        self.save()


#TODO: refactor signals to signals.py in hitmeup app

IMAGE_SIZE = 200

@receiver(request_friend, sender=UserProfile)
def send_friend_request_notification(sender, from_friend, to_friend, **kwargs):
    # Don't duplicate notifications
    notification, created = Notification.objects.get_or_create(
        recipient=to_friend,
        image_url=from_friend.get_gravatar_url(IMAGE_SIZE),
        action_url=from_friend.profile_url,
        text=Notification.NOTIFICATION_STRINGS[Notification.REQUEST_FRIEND] % from_friend,
    )
    if created:
        send_notification_email(notification)

    if not created:
        notification.refresh()

@receiver(accept_friend, sender=UserProfile)
def send_friend_accept_notification(sender, from_friend, to_friend, **kwargs):
    # Don't duplicate notifications
    notification, created = Notification.objects.get_or_create(
        recipient=to_friend,
        image_url=from_friend.get_gravatar_url(IMAGE_SIZE),
        action_url=from_friend.profile_url,
        text=Notification.NOTIFICATION_STRINGS[Notification.ACCEPT_FRIEND] % from_friend,
    )
    if created:
        send_notification_email(notification)

    if not created:
        notification.refresh()
