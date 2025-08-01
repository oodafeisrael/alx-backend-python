from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(post_save, sender=Message)
def notify_receiver_on_message(sender, instance, created, **kwargs):
    """
    Creates a notification for the receiver when a new message is sent.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender.username}"
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs old content of a message before it's updated.
    """
    if instance.pk:  # Editing an existing message
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    original_message=old_instance,
                    previous_content=old_instance.content,
                    edited_by=instance.sender
                )
        except Message.DoesNotExist:
            pass  # No old message exists (shouldn't happen in practice)

@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """
    Automatically delete all messages, notifications, and message histories 
    related to a user when their account is deleted.
    
    Args:
        sender (Model): The model class sending the signal (User).
        instance (User): The user instance being deleted.
        **kwargs: Additional keyword arguments.
    """
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications associated with user
    Notification.objects.filter(user=instance).delete()

    # Delete message history for user’s messages
    MessageHistory.objects.filter(original_message__sender=instance).delete()
