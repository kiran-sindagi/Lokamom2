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
        
        # 1. Skip logging for ignored paths or requests without a session
        path = request.path
        if any(path.startswith(p) for p in self.IGNORED_PATHS) or not hasattr(request, 'session'):
            return self.get_response(request)

        # Ensure the session key is created if it's new
        if not request.session.session_key:
            request.session.create()
            
        session_key = request.session.session_key
        user = request.user if request.user.is_authenticated else None
        
        # 2. Check if a visit was already logged in the last minute (to avoid logging every internal page load)
        # This is a common method to count "Page Views" versus "Visits"
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        
        # Filter logic: Check if this user/session has visited this path recently
        if user:
            recent_visits = Visit.objects.filter(user=user, path=path, timestamp__gte=one_minute_ago).exists()
        else:
            recent_visits = Visit.objects.filter(session_key=session_key, path=path, timestamp__gte=one_minute_ago).exists()
            
        
        if not recent_visits:
            # 3. Log the new visit
            Visit.objects.create(
                user=user,
                session_key=session_key,
                path=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=self._get_client_ip(request)
            )
            
            # 4. Update or create the UniqueVisitor record
            self._update_unique_visitor(user, session_key)

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

    def _update_unique_visitor(self, user, session_key):
        """Updates the last_visit time for a unique visitor."""
        try:
            if user:
                # Visitor is authenticated
                obj, created = UniqueVisitor.objects.get_or_create(
                    user=user,
                    defaults={'session_key': session_key}
                )
            else:
                # Visitor is anonymous
                obj, created = UniqueVisitor.objects.get_or_create(
                    session_key=session_key,
                    defaults={'user': None}
                )

            if not created:
                obj.last_visit = datetime.now()
                obj.save(update_fields=['last_visit'])

        except Exception as e:
            # Log the exception for debugging
            print(f"Error updating UniqueVisitor: {e}")
