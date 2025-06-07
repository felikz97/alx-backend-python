# chats/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse

logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')  # <- This file
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply restriction on /chats/ path (optional)
        if request.path.startswith('/chats/'):
            now = datetime.now().time()
            allowed_start = now.replace(hour=18, minute=0, second=0, microsecond=0)
            allowed_end = now.replace(hour=21, minute=0, second=0, microsecond=0)

            if not (allowed_start <= now <= allowed_end):
                return HttpResponseForbidden("Access to chats is restricted outside 6PM–9PM")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_tracker = {}  # {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        if request.path.startswith('/chat/') and request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = time.time()
            request_times = self.ip_tracker.get(ip, [])

            # Filter timestamps within the last 60 seconds
            request_times = [t for t in request_times if current_time - t < 60]

            if len(request_times) >= 5:
                return JsonResponse(
                    {'error': 'Rate limit exceeded: Max 5 messages per minute'},
                    status=429
                )

            request_times.append(current_time)
            self.ip_tracker[ip] = request_times

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Optional: scope to certain endpoints like /chat/
        if request.path.startswith('/chat/'):
            if request.user.is_authenticated:
                role = getattr(request.user, 'role', None)
                if role not in ['admin', 'moderator']:
                    return HttpResponseForbidden("403 Forbidden: Insufficient permissions.")
            else:
                return HttpResponseForbidden("403 Forbidden: Authentication required.")
        
        return self.get_response(request)