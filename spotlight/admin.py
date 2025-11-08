from django.contrib import admin
from .models import WomenInSpotlight 

@admin.register(WomenInSpotlight)
class ProfileAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Profile model in the Django admin.
    """
    list_display = ('name', 'description', 'picture')
    search_fields = ('name', 'description')