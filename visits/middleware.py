from .models import Visit, UniqueVisitor
from django.conf import settings
from datetime import datetime, timedelta

class VisitTrackingMiddleware:
    """
    Middleware to log every unique request as a visit.
    It requires SessionMiddleware and AuthenticationMiddleware to run before it.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Define a list of paths (or path prefixes) to ignore, like static files
        self.IGNORED_PATHS = [
            '/admin/', 
            '/static/', 
            '/media/', 
            '/favicon.ico',
        ]
        
    def __call__(self, request):
        # 1. Skip logging for ignored paths
        path = request.path
        if any(path.startswith(p) for p in self.IGNORED_PATHS):
            return self.get_response(request)

        user = request.user if request.user.is_authenticated else None
        ip_address = self._get_client_ip(request)
        
        # 2. Check if a visit was already logged in the last minute
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        
        # Filter logic: Check if this IP address has visited this path recently
        if user:
            recent_visits = Visit.objects.filter(user=user, path=path, timestamp__gte=one_minute_ago).exists()
        else:
            recent_visits = Visit.objects.filter(ip_address=ip_address, path=path, timestamp__gte=one_minute_ago).exists()
            
        if not recent_visits:
            # 3. Log the new visit
            Visit.objects.create(
                user=user,
                session_key=request.session.session_key if hasattr(request, 'session') else None,
                path=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=ip_address
            )
            
            # 4. Update or create the UniqueVisitor record
            self._update_unique_visitor(user, ip_address)

        response = self.get_response(request)
        return response

    def _get_client_ip(self, request):
        """Attempts to get the client's real IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # IP addresses can be a comma-separated list of IPs.
            # The client's IP is typically the first one.
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _update_unique_visitor(self, user, ip_address):
        """Updates the last_visit time for a unique visitor based on IP."""
        try:
            if user:
                # Visitor is authenticated
                obj, created = UniqueVisitor.objects.get_or_create(
                    user=user,
                    defaults={'ip_address': ip_address}
                )
            else:
                # Visitor is anonymous
                obj, created = UniqueVisitor.objects.get_or_create(
                    ip_address=ip_address,
                    defaults={'user': None}
                )

            if not created:
                obj.last_visit = datetime.now()
                obj.save(update_fields=['last_visit'])

        except Exception as e:
            print(f"Error updating UniqueVisitor: {e}")
