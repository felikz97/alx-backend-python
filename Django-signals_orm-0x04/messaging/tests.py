# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass')
        self.receiver = User.objects.create_user(username='bob', password='pass')

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello Bob!')
        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_message_edit_logs_history(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Original message')
        message.content = 'Edited message'
        message.save()
        history = MessageHistory.objects.filter(message=message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, 'Original message')
        self.assertTrue(message.edited)