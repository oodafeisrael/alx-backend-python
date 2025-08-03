from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from .forms import MessageForm

User = get_user_model()


def inbox(request):
    """Display all top-level messages received by the user."""
    messages = Message.objects.filter(
        receiver=request.user,
        parent=None
    ).select_related('sender').prefetch_related('replies')

    return render(request, 'messaging/inbox.html', {'messages': messages})


def get_threaded_replies(message):
    """Recursively fetch all replies to a message."""
    replies = message.replies.select_related('sender').all()
    for reply in replies:
        reply.child_replies = get_threaded_replies(reply)
    return replies


def message_detail(request, message_id):
    """View a single message and all of its replies (threaded)."""
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies__sender'),
        id=message_id
    )

    threaded_replies = get_threaded_replies(message)

    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'threaded_replies': threaded_replies,
    })


def send_message(request, receiver_id=None, parent_id=None):
    """Send a new message or reply."""
    receiver = None
    parent = None

    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)
    if parent_id:
        parent = get_object_or_404(Message, id=parent_id)
        receiver = parent.sender  # reply goes to sender of original message

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = receiver
            msg.parent = parent
            msg.save()
            return redirect('messaging:inbox')
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {
        'form': form,
        'receiver': receiver,
        'parent': parent,
    })

def view_message(request, message_id):
    """
    View a single message and all of its threaded replies using a recursive structure.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                       .prefetch_related('replies'),
        id=message_id
    )

    if not message.read:
        message.read = True
        message.save(update_fields=['read'])

    return render(request, 'messaging/view_message.html', {'message': message})

    def get_thread(message):
        """
        Recursively fetch all replies to a message.
        """
        thread = []
        for reply in message.replies.all():
            thread.append({
                'message': reply,
                'replies': get_thread(reply)
            })
        return thread

    context = {
        'message': message,
        'threaded_replies': get_thread(message)
    }
    return render(request, 'messaging/view_message.html', context)

@login_required
def reply_message(request, message_id):
    parent = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(
                sender=request.user,
                recipient=parent.sender,
                body=body,
                parent_message=parent,
            )
            return redirect('messaging:inbox')  # Or wherever you want to redirect

    return render(request, 'messaging/reply_message.html', {'parent': parent})

@login_required
def unread_messages_view(request):
    """
    Display unread messages for the logged-in user.
    Only necessary fields are fetched using `.only()` for performance.
    """
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'content', 'timestamp'
    )
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })
