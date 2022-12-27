from common.models import SoftDeletionModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(SoftDeletionModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_zone = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        default="US/Eastern",
        verbose_name="Time Zone",
    )

    def __str__(self):
        if self.user.get_full_name() != "":
            return self.user.get_full_name()
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
