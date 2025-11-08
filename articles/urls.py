from django.urls import path
from . import views
from forums.views import send_reply

urlpatterns = [
    path('', views.SectionsView.as_view(), name='articles'),
    path('section/<str:section>/', views.ArticlesListView.as_view(), name='section_articles'),
    path('article/<int:pk>/', views.readArticle, name="read_article"),
    path('forums/post/<int:pk>/', send_reply, name="questions")
]
