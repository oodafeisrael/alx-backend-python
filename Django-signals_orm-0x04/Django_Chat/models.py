"""
models.py for Django-Chat application.

Implements the Message model with threading support using a self-referential
foreign key, optimized ORM access, and recursive reply retrieval.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    """
    Represents a message between users. Supports threading through
    a self-referential foreign key to represent replies.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages_chat")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages_chat")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # Self-referential FK for threading
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:30]}"

    def get_all_replies(self):
        """
        Recursively fetches all replies to this message.

        Returns:
            list: A flat list of Message instances that are replies.
        """
        all_replies = []

        for reply in self.replies.select_related('sender', 'receiver').all():
            all_replies.append(reply)
            all_replies.extend(reply.get_all_replies())  # recursive

        return all_replies

    @classmethod
    def get_threaded_message(cls, message_id):
        """
        Retrieve a message with its replies using optimized ORM queries.

        Args:
            message_id (int): ID of the root message

        Returns:
            Message: The root message with preloaded related data
        """
        return cls.objects.select_related('sender', 'receiver', 'parent_message') \
                          .prefetch_related('replies__sender', 'replies__receiver') \
                          .get(id=message_id)

