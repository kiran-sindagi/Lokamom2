from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contribute/', views.contribute, name='contribute'),
    path('successful/', views.successful, name='successful'),
    path('contact-us/', views.contact, name='contact-us'),
    path('work_career/', views.workCareer, name='work_career')
]
