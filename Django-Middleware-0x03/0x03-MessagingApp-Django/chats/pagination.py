# chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class ChatPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to override
    max_page_size = 100  # Prevent abuse
