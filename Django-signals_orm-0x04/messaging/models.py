from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager


User = get_user_model()


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to retrieve unread messages for a specific user.
    Optimized with `.only()` to fetch only essential fields.
    """
    def for_user(self, user):
        return self.filter(recipient=user, read=False).only(
            'id', 'sender', 'recipient', 'subject', 'sent_at'
        )


class Message(models.Model):
    """
    Represents a message sent from one user to another.
    
    Fields:
        sender (User): The user who sends the message.
        receiver (User): The user who receives the message.
        content (str): The body of the message.
        timestamp (datetime): The time the message was created.
        edited (bool): Whether the message has been edited.
        parent_message (Message): A self-referential link to support message replies (threading).
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies',
        help_text="Reference to the parent message if this message is a reply."
    )
    
    """Field to track if message is read"""
    read = models.BooleanField(default=False)

    read = models.BooleanField(default=False)
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:20]}"

    def get_all_replies(self):
        """
        Recursively retrieves all replies to this message in a threaded structure.

        Returns:
            list: A nested list of replies represented as dictionaries.
        """
        def build_thread(message):
            return {
                'id': message.id,
                'content': message.content,
                'sender': message.sender.username,
                'replies': [build_thread(reply) for reply in message.replies.all()]
            }
        return build_thread(self)


class Notification(models.Model):
    """
    Represents a notification for a user when a new message is received.
    
    Fields:
        user (User): The user who receives the notification.
        message (Message): The associated message.
        is_read (bool): Whether the notification has been read.
        timestamp (datetime): The time the notification was created.
    """
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"


class MessageHistory(models.Model):
    """
    Stores historical content of messages that have been edited.
    
    Fields:
        message (Message): The original message that was edited.
        old_content (str): The previous content of the message before editing.
        edited_at (datetime): The time the message was edited.
    """
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for Message ID {self.message.id} at {self.edited_at}"

