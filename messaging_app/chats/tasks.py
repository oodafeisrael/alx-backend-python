from celery import shared_task
from django.core.mail import send_mail
from .models import Message

@shared_task
def notify_user_new_message(message_id):
    """
    Celery task to notify a user that they have received a new message.
    You could send an email, push notification, or log it.
    """
    try:
        message = Message.objects.get(id=message_id)
        recipient_email = message.recipient.email
        subject = f"New message from {message.sender.username}"
        body = f"You received a new message:\n\n{message.content}"

        # Example email sending logic
        send_mail(
            subject,
            body,
            'noreply@yourapp.com',  # Replace with your sender email
            [recipient_email],
            fail_silently=False,
        )
        return f"Notification sent to {recipient_email}"
    
    except Message.DoesNotExist:
        return f"Message with ID {message_id} does not exist."

    except Exception as e:
        return f"Error sending notification: {str(e)}"
