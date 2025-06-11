# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.http import HttpResponse, request
from django.db.models import Prefetch, Q, Count, F

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')
# adjust redirect target as needed
# messaging/views.py


def home(request):
    return HttpResponse("Hello, World!")
# messaging/views.py

def user_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})
# messaging/views.py

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})
# messaging/views.py


def user_messages(request, username):
    user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(receiver=user).order_by('-timestamp')
    notifications = Notification.objects.filter(user=user, is_read=False)
    
    return render(request, 'user_messages.html', {
        'user': user,
        'messages': messages,
        'notifications': notifications
    })


@login_required
def user_threaded_messages(request):
    user = request.user
    sender = request.user
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_message_id = request.POST.get('parent_message_id')
        parent_message = None
        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)
        
        message = Message.objects.create(sender=sender, receiver=user, content=content, parent_message=parent_message)
        Notification.objects.create(user=user, message=message)
    messages = Message.objects.filter(receiver=user, parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('-timestamp')
    return render(request, 'messaging/threaded_messages.html', {'messages': messages})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('user_messages', username=request.user.username)