import logging
from datetime import datetime

# Configure the logger to write to 'requests.log' in the project root.
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    """
    Middleware that logs each incoming HTTP request with timestamp, user, and path.

    This middleware writes to 'requests.log' in the format:
    'YYYY-MM-DD HH:MM:SS.microseconds - User: <username/Anonymous> - Path: <URL path>'
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the next callable in the stack.

        Args:
            get_response (callable): The next middleware or view to call.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Handle the request, log the necessary information, then continue processing.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The response returned by the view or next middleware.
        """
        # Determine user identity
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"

        # Log the request information
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response

