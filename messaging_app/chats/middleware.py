# chats/middleware.py

from django.http import JsonResponse

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip check for unauthenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Get user role — assuming it's a field on the user model
        user_role = getattr(request.user, 'role', None)

        # Only allow admin or moderator
        if user_role not in ['admin', 'moderator']:
            return JsonResponse({'detail': 'Forbidden: Insufficient role permissions'}, status=403)

        return self.get_response(request)
