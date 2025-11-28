from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

from django.db.models.signals import pre_save
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_edit(sender, instance, **kwargs):
    if instance.id:  # means message already exists
        old_msg = Message.objects.get(id=instance.id)
        if old_msg.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_msg.content
            )
            instance.edited = True

from django.contrib.auth.models import User
from django.db.models.signals import post_delete

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
