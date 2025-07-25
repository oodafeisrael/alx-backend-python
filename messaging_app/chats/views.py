from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'message_set')
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expected POST body:
        {
            "participants": [user_id1, user_id2]
        }
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "A conversation requires at least two participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() < 2:
            return Response(
                {"error": "One or more participant IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to a conversation.
        Expected POST body:
        {
            "conversation_id": "uuid",
            "sender_id": "uuid",
            "message_body": "Hello there"
        }
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not all([conversation_id, sender_id, message_body]):
            return Response(
                {"error": "conversation_id, sender_id, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        if sender not in conversation.participants.all():
            return Response(
                {"error": "Sender is not a participant in the conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
