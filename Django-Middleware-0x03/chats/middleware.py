from datetime import datetime
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        with open("requests.log", "a") as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        if not (18 <= now <= 21):
            return HttpResponseForbidden("Chat access is restricted between 9PM and 6PM")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/api/conversations"):
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_requests.get(ip, [])
            timestamps = [t for t in timestamps if now - t < 60]
            if len(timestamps) >= 5:
                return HttpResponseForbidden("Too many messages sent. Try again later.")
            timestamps.append(now)
            self.ip_requests[ip] = timestamps
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_paths = ["/api/admin-only"]
        if request.path in admin_paths:
            if not request.user.is_authenticated or request.user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        response = self.get_response(request)
        return response

