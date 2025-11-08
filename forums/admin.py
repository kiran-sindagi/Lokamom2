from django.contrib import admin # type: ignore
from .models import Post, Reply
# Register your models here.

class ReplyInline(admin.StackedInline): # new
    model = Reply
class PostAdmin(admin.ModelAdmin): # new
    inlines = [
        ReplyInline,
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Reply)