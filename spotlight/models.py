from django.db import models

class WomenInSpotlight(models.Model):
    """
    Represents a profile with a name, picture, and description.
    """
    name = models.CharField(max_length=100, help_text="The name of the person or item.")
    picture = models.ImageField(upload_to='profile_pictures/', help_text="An image for the profile.")
    description = models.TextField(help_text="A detailed description for the profile.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "WomenInSpotlight"
        verbose_name_plural = "WomenInSpotlight"