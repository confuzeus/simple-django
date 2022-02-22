import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_django.core.models import UserProfile

User = get_user_model()

log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save_actions(sender, instance, created, **kwargs):

    if created:
        # User profile
        profile = UserProfile(user=instance)
        profile.save()
        log.info(f"Created {str(profile)}")
