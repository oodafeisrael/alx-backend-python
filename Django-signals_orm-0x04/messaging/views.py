from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def inbox(request):
    """
    View to display the inbox for the logged-in user, showing all top-level messages (non-replies).
    Uses select_related and prefetch_related to optimize DB queries.
    """
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender').all(),
                to_attr='prefetched_replies'
            )
        )
        .order_by('-timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def message_detail(request, message_id):
    """
    View to display a specific message thread, including all nested replies.
    Uses recursion to build a threaded reply chain.
    """
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver'), id=message_id)

    def get_all_replies(parent):
        """
        Recursively fetch all replies to a given message.
        """
        replies = Message.objects.filter(parent_message=parent).select_related('sender', 'receiver')
        thread = []
        for reply in replies:
            nested_replies = get_all_replies(reply)
            thread.append((reply, nested_replies))
        return thread

    all_replies = get_all_replies(message)

    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'replies': all_replies
    })
  
