import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden


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


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app outside 6PM–9PM.
    
    If the current time is outside the allowed window, it returns a 403 Forbidden response.
    """
    def __init__(self, get_response):
        """
        Store the middleware's get_response callable.
        
        Args:
            get_response (Callable): The next middleware or view to be called.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Check if the current time is between 6PM and 9PM (inclusive).
        Deny access (403) if outside this range.
        
        Args:
            request (HttpRequest): The incoming HTTP request.
            
        Returns:
            HttpResponse: Either the forbidden response or the next middleware/view.
        """
        # Define allowed time range
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM
        now = datetime.now().time()

        # Check if current time is within allowed time range
        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access to the messaging app is only allowed between 6PM and 9PM.")

        # Continue processing the request
        return self.get_response(request)
