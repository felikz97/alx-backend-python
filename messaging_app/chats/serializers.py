from rest_framework import serializers
from .models import CustomUser, Conversation, Message


# --- USER SERIALIZER ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']

# --- MESSAGE SERIALIZER ---
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']
# --- NESTED MESSAGE SERIALIZER (for use in conversation) ---
class NestedMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
# --- CONVERSATION SERIALIZER ---

# --- CONVERSATION SERIALIZER WITH NESTED MESSAGES ---
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = NestedMessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']


# --- CONVERSATION CREATE SERIALIZER (to accept participant IDs) ---
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants']

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
# --- MESSAGE CREATE SERIALIZER (to accept conversation ID and sender ID) ---