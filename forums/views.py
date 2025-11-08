from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.views.generic import ListView, DetailView, CreateView, DeleteView # type: ignore
from .models import Post, Reply
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect, Http404 # type: ignore
from django.utils import timezone # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib import messages # type: ignore
from django.urls import reverse_lazy 
from django.db.models import Q 
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'forumPages/forum.html'
    paginate_by = 10
    context_object_name = "items"
    def get_queryset(self):
        return Post.objects.all().order_by('-id')

import pytz # type: ignore 


@login_required
def create_post(request):
    if request.method == 'POST':
        body = request.POST.get('quest')

        # Get user's timezone from cookies, fallback to UTC
        user_timezone = request.COOKIES.get("user_timezone", "UTC")
        try:
            user_tz = pytz.timezone(user_timezone)
        except pytz.UnknownTimeZoneError:
            user_tz = pytz.UTC  # If invalid, default to UTC

        # Get current time in user's timezone
        local_time = timezone.now().astimezone(user_tz)
        local_date = timezone.now().astimezone(user_tz).date()

        if body:
            post = Post(body=body, owner=request.user, time=local_time, date = local_date)
            post.save()
            return redirect('forums')

    return render(request, "forumPages/ask_question.html")

@login_required
def send_reply(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        user_timezone = request.COOKIES.get("user_timezone", "UTC")
        try:
            user_tz = pytz.timezone(user_timezone)
        except pytz.UnknownTimeZoneError:
            user_tz = pytz.UTC

        local_time = timezone.now().astimezone(user_tz)
        local_date = timezone.now().astimezone(user_tz).date()
        if reply.strip():
            reply = Reply(reply=reply, owner = request.user, post = post, time = local_time, date = local_date)
            reply.save()
            return redirect("question_detail", pk=pk)
    all_replies = post.replys.all().order_by('-date', '-time')
    paginator = Paginator(all_replies, 5)  # 5 replies per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'post': post, 'page_obj':page_obj}
    return render(request,"forumPages/detail.html", context)

class YourPostsView(ListView):
    model = Post
    template_name = 'profilePages/yourPosts.html'
    paginate_by = 10
    context_object_name = "items"
    def get_queryset(self):
        return Post.objects.all().order_by('-id')

@method_decorator(never_cache, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'profilePages/deletePosts.html'
    success_url = reverse_lazy('yourPosts')

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Optionally, add a message here
            return redirect('yourPosts')

class SearchPostView(ListView):
    model = Post
    template_name = 'forumPages/search.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Post.objects.filter(Q(body__icontains=query) | Q(owner__username__icontains=query)) if query else Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context