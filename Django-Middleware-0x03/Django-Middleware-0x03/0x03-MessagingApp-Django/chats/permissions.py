# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Allows GET, HEAD, OPTIONS for anyone,
    and PUT, PATCH, DELETE for owners only.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user
        return False


from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to access messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Called for object-level permissions (e.g., retrieving, updating or deleting a message)
        Assumes obj is a Message instance
        """
        # Only participants of the conversation can access the message
        return request.user in obj.conversation.participants.all()
