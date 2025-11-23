import logging
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden

# Logger for request logging
logging.basicConfig(filename='requests.log', level=logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hour = datetime.now().hour
        if not (18 <= hour <= 21):  # Access allowed only between 6PM and 9PM
            return HttpResponseForbidden("Chat allowed only between 6PM and 9PM")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_data = defaultdict(list)  # Track requests per IP

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            now = time.time()
            # Keep only requests in the last 60 seconds
            self.ip_data[ip] = [t for t in self.ip_data[ip] if now - t < 60]

            if len(self.ip_data[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded")

            self.ip_data[ip].append(now)

        return self.get_response(request)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            role = getattr(request.user, "role", "user")
            if role not in ["admin", "moderator"]:
                return HttpResponseForbidden("Forbidden")
        else:
            return HttpResponseForbidden("Forbidden")

        return self.get_response(request)
