from rest_framework import viewsets, permissions, filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationCreateSerializer,
    MessageCreateSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_serializer_class(self):
        return ConversationCreateSerializer if self.action == 'create' else ConversationSerializer

    def perform_create(self, request, serializer):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        # Only return messages from conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_serializer_class(self):
        return MessageCreateSerializer if self.action == 'create' else MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.validated_data['conversation']
            if request.user not in conversation.participants.all():
                return Response({"detail": "You are not a participant in this conversation."},
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)