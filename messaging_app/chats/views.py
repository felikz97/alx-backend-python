from rest_framework import viewsets, permissions, filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationCreateSerializer,
)


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
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    

    def get_serializer_class(self):
        return MessageCreateSerializer if self.action == 'create' else MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Filter only messages where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Only allow creation if user is a participant
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)