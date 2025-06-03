# chats/middleware.py

import logging
from datetime import datetime
import os

# Configure logger
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', 'requests.log')
file_handler = logging.FileHandler(os.path.abspath(log_path))
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        timestamp = datetime.now()

        logger.info(f"{timestamp} - User: {user} - Path: {path}")

        response = self.get_response(request)
        return response

#-------------------------------------------------------------------
# chats/middleware.py


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        log_path = os.path.join(os.path.dirname(__file__), '..', 'requests.log')
        logging.basicConfig(
            filename=os.path.abspath(log_path),
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)

        response = self.get_response(request)
        return response
