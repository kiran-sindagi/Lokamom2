# articles/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Articles
from forums.models import Post  # cross-app import
from django.utils import timezone
from datetime import datetime, timedelta



@receiver(post_save, sender=Articles)
def create_post_from_article(sender, instance, created, **kwargs):
    if created:
        local_time = timezone.now()
        local_time = local_time - timedelta(hours=6, minutes=30)
        local_date = timezone.now().date()
        Post.objects.create(
            body= instance.question,  # adjust according to field names
            owner= instance.owner,
            time = local_time,
            date = local_date
        )
