# messaging/signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:
        try:
            original = Message.objects.get(pk=instance.id)
            if original.content != instance.content:
                MessageHistory.objects.create(message=instance, old_content=original.content)
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:
        try:
            original = Message.objects.get(pk=instance.id)
            if original.content != instance.content:
                MessageHistory.objects.create(message=instance, old_content=original.content)
                instance.edited = True
                instance.edited_by = instance.sender  # default to sender if no editor context
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

@receiver(post_save, sender=Notification)
def mark_notification_as_read(sender, instance, **kwargs):
    if instance.is_read:
        instance.save()
        