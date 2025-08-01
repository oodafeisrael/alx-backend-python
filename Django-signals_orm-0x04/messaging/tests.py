from django.test import TestCase


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingSignalTestCase(TestCase):
    """
    Test case for verifying that a Notification is automatically
    created whenever a new Message is sent.
    """

    def setUp(self):
        """
        Set up test users before each test case.
        """
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password123')

    def test_notification_created_on_message_send(self):
        """
        Test that a Notification object is created for the receiver
        when a Message object is created.
        """
        # Create a message from alice to bob
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Bob!'
        )

        # Ensure a notification is created
        self.assertEqual(Notification.objects.count(), 1)

        # Validate the notification details
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message.content, 'Hello Bob!')
