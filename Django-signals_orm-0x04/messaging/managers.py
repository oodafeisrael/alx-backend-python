from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to retrieve unread messages for a specific user.
    Usage: Message.unread.for_user(user)
    """

    def for_user(self, user):
        return self.get_queryset().filter(
            recipient=user,
            read=False
        ).only('id', 'sender', 'content', 'timestamp')  # optimized with .only()

