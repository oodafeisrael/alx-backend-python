import time
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


class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages (POST requests) sent by each IP address
    within a 1-minute window. If an IP sends more than 5 messages within a minute,
    further messages will be blocked with a 429 Too Many Requests error.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with a response handler and an in-memory store
        to track requests per IP address.
        """
        self.get_response = get_response
        self.ip_request_log = {}  # Format: {ip: [timestamp1, timestamp2, ...]}

    def __call__(self, request):
        """
        Checks the number of POST requests from an IP address in the past minute.
        Blocks the request if the limit is exceeded.
        """
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than 1 minute
            timestamps = self.ip_request_log.get(ip, [])
            timestamps = [t for t in timestamps if now - t < 60]

            if len(timestamps) >= 5:
                return JsonResponse({
                    "error": "Rate limit exceeded. Only 5 messages allowed per minute."
                }, status=429)

            timestamps.append(now)
            self.ip_request_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Retrieves the IP address of the client making the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
