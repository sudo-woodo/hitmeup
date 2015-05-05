from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from user_accounts.models import UserProfile


# Auto-create a UserProfile when creating a User
# https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
