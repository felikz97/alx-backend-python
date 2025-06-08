from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested import routers


# Root router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router: messages under conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')
router.register(r'conversations/(?P<conversation_id>\d+)/messages', MessageViewSet, basename='messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    
]