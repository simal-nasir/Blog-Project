from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserAccount
from blogApp.models import Profile

@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserAccount)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()