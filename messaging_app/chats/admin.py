from django.contrib import admin
from .models import CustomUser, Conversation, Message
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'phone_number')
    search_fields = ('email', 'first_name', 'last_name')    
# Register your models here.

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    search_fields = ('conversation_id',)
    filter_horizontal = ('participants',)    
    list_filter = ('created_at',)