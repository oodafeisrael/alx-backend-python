from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Stores the previous content of a message into MessageHistory
    if the message content is being changed (i.e., edited).
    """
    if instance.id:
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:
                # Log the old message content before editing
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.edited = True  # Mark message as edited
        except Message.DoesNotExist:
            pass
