from django.db import models # type: ignore
from django.urls import reverse # type: ignore
 # type: ignore
from django.utils.timezone import now # type: ignore
from articles.models import Articles
from datetime import datetime
# Create your models here.

class Post(models.Model):
    time = models.TimeField(null=True, blank=True)
    date = models.DateField()
    body = models.TextField()
    owner = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return self.body
    
class Reply(models.Model):
    time = models.TimeField()
    date = models.DateField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replys',)
    reply = models.TextField()
    owner = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return self.reply
    
    def get_absolute_url(self):
        return reverse("question_detail")
    