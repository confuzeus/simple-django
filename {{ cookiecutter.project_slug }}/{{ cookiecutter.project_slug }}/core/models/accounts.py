from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):

    class Meta:
        ordering = ["-date_joined"]
        db_table = "users"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self):
        return f"{self.user.email}'s profile."

    class Meta:
        ordering = ["-user__date_joined"]
        db_table = "user_profiles"
