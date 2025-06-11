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
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # adjust redirect target as needed

@login_required
def user_threaded_messages(request):
    user = request.user
    messages = Message.objects.filter(receiver=user, sender=request.user, parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('-timestamp')
    return render(request, 'messaging/threaded_messages.html', {'messages': messages})


@login_required
def unread_inbox(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})