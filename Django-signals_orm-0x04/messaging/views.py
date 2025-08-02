from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch
from django.contrib.auth import get_user_model

User = get_user_model()


@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    """
    View to delete the currently logged-in user and trigger cleanup of related data.
    """
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({'message': f'User {username} deleted successfully.'}, status=200)

@login_required
def send_message(request):
    """
    Handle sending a message from the logged-in user to another user.
    """
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # For replies (optional)

        if not receiver_id or not content:
            return HttpResponseBadRequest("Missing required fields.")

        receiver = get_object_or_404(User, pk=receiver_id)
        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, pk=parent_id)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        return redirect('inbox')  # replace with your desired redirect view

    return render(request, 'messaging/send_message.html')


@login_required
def inbox(request):
    """
    Display all messages received by the logged-in user, with replies prefetched.
    """
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender'))
        )
        .order_by('-timestamp')
    )

    return render(request, 'messaging/inbox.html', {'messages': messages})

