from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from communications.emails import send_registration_email
from user_accounts.models import UserProfile


class Subscription(models.Model):
    profile = models.OneToOneField(UserProfile, primary_key=True, related_name='subscription')

    general = models.BooleanField(default=True)
    friend_notifications = models.BooleanField(default=True)

    def __unicode__(self):
        return self.profile.username

# Auto-create a Subscription when creating a UserProfile
@receiver(post_save, sender=UserProfile)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(profile=instance)
        # Send welcome email when profile is created
        send_registration_email(instance)
