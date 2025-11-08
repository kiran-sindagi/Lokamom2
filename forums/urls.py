from django.urls import path # type: ignore
from .views import PostListView, YourPostsView, PostDeleteView, SearchPostView
from . import views
urlpatterns = [
    path('',PostListView.as_view(), name = 'forums'),
    path('post/<int:pk>/', views.send_reply, name="question_detail"),
    path('post/new', views.create_post, name='ask_question'),
    path('your-posts', YourPostsView.as_view(), name="yourPosts" ),
    path('delete-post/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('search/', SearchPostView.as_view(), name='search_post')
]
