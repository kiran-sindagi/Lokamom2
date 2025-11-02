from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkCareerView, name="work_career_form"),
]
