from django.urls import path, include
from .admin import analytics_admin_site

urlpatterns = [
    path('', analytics_admin_site.urls),
]