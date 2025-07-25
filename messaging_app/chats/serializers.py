from rest_framework import serializers
from .models import User, Message, Conversation


from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(source='message_set', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages'
        ]
        read_only_fields = ['conversation_id', 'created_at']


