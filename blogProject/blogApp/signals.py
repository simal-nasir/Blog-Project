from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from .models import *

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=BlogPost)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscriptions = Subscription.objects.filter(
            Q(category=instance.category) |
            Q(tag__in=instance.tags.all()) |
            Q(author=instance.author)
        ).select_related('user')

        for subscription in subscriptions:
            send_mail(
                subject='New Blog Post Update!',
                message=f'A new post titled "{instance.title}" has been published.',
                from_email='simalnasir1@gmail.com',
                recipient_list=[subscription.user.email],
            )