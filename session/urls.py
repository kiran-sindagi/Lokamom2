from django.urls import path
from . import views

urlpatterns = [
    path('', views.Letter, name="letter"),
    path('what-we-offer/', views.whatWeOffer, name="session"),
    path("one-on-one/", views.oneOnOne, name="one"),
    path("group-sessions/", views.groupSession, name="group"),
    path("stress-management", views.StressSession, name="stress"),
    path('book-one-on-one/', views.oneToOne_view, name='book-One-on-One'),
    path('book-group-session/', views.groupSession_view, name='book-group-session'),
    path('book-stress-management-session/', views.stressSession_view, name='book-stress-session'),
    path('success/', views.success_view, name='success_page'),
    path('failure/', views.failure_view, name='failure_page')
]
