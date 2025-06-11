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
        
    def test_user_deletion_cleans_up_data(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Will be deleted')
        Notification.objects.create(user=self.receiver, message=message)
        message.content = 'Edit before delete'
        message.save()
        self.sender.delete()
        self.assertFalse(Message.objects.filter(id=message.id).exists())
        self.assertFalse(Notification.objects.exists())
        self.assertFalse(MessageHistory.objects.exists())
    def test_notification_read_status(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Check this out!')
        notification = Notification.objects.create(user=self.receiver, message=message)
        self.assertFalse(notification.is_read)
        
        # Mark notification as read
        notification.is_read = True
        notification.save()
        
        # Verify the status
        updated_notification = Notification.objects.get(id=notification.id)
        self.assertTrue(updated_notification.is_read)
    
    def test_threaded_conversation(self):
        root = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Root message')
        reply1 = Message.objects.create(sender=self.receiver, receiver=self.sender, content='Reply 1', parent_message=root)
        reply2 = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Reply 2', parent_message=reply1)
        replies = root.get_all_replies()
        self.assertIn(reply1, replies)
        self.assertIn(reply2, replies)
        self.assertEqual(len(replies), 2)