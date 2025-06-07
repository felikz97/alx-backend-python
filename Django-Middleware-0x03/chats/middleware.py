# myapp/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden

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