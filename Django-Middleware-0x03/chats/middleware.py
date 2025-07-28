"""
Middleware module for logging user requests to a log file.

This middleware captures each incoming request, records the timestamp, 
the user (or 'Anonymous' if not authenticated), and the requested path. 
The data is logged into a file called `requests.log`.

Example log entry:
    2025-07-26 18:42:03.321243 - User: Anonymous - Path: /
"""

import logging
from datetime import datetime

# Set up logger for this middleware
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware class that logs details of every HTTP request made to the server.

    Attributes:
        get_response (callable): The next middleware or view in the Django request/response cycle.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with the next layer in the stack.

        Args:
            get_response (callable): The next middleware or view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Called on each request before the view (and later middleware) is called.

        Logs the current timestamp, username (or 'Anonymous'), and the request path.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The response from the view or next middleware.
        """
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response

