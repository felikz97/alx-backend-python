# messaging/models.py
from django.db import models
from django.contrib.auth.models import User

from .managers import UnreadMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    read = models.BooleanField(default=False)

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_all_replies(self):
        replies = []
        def recursive_fetch(message):
            for reply in message.replies.all():
                replies.append(reply)
                recursive_fetch(reply)
        recursive_fetch(self)
        return replies

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID: {self.message.id}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='parent_history', null=True, blank=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='message_history')
    parent_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f"Edit history for Message ID: {self.message.id} at {self.edited_at}"