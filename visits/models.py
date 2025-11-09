from django.db import models
from django.conf import settings

# Get the User model dynamically, handles custom user models
User = settings.AUTH_USER_MODEL 

class Visit(models.Model):
    """
    Tracks individual website visits.
    A visit is identified by a unique session key.
    """
    # Required for the AuthenticationMiddleware to work correctly
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             verbose_name="Authenticated User")
    
    # Session key is the unique identifier for anonymous visitors
    session_key = models.CharField(max_length=40, db_index=True, verbose_name="Session Key")
    
    # The URL path the user visited
    path = models.CharField(max_length=255, verbose_name="Path Visited")
    
    # Timestamp of the visit
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Time of Visit")
    
    # Additional metadata (User Agent, IP Address)
    user_agent = models.CharField(max_length=255, blank=True, null=True, verbose_name="User Agent")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")

    class Meta:
        verbose_name = "Website Visit"
        verbose_name_plural = "Website Visits"
        ordering = ['-timestamp']
        
    def __str__(self):
        # Display the user or session key if user is anonymous
        identifier = self.user.username if self.user else f"Session: {self.session_key[:8]}..."
        return f"Visit by {identifier} to {self.path} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def get_user_identifier(self):
        """Helper for Admin display."""
        if self.user:
            return self.user.username
        if self.session_key:
            return f"Anonymous ({self.session_key[:8]})"
        return "Unknown"
    get_user_identifier.short_description = 'Visitor'

# Optional: Model to store aggregated data (e.g., daily unique visitors)
class UniqueVisitor(models.Model):
    """
    Keeps track of unique visitors by IP address or user ID.
    """
    ip_address = models.GenericIPAddressField(unique=True, db_index=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Unique Visitor"
        verbose_name_plural = "Unique Visitors"
        
    def __str__(self):
        return self.user.username if self.user else f"IP: {self.ip_address}"
