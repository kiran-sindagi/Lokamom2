from django.urls import path
from .views import WomenInSpotlight_list, ContactUs_view # This line is commented out

urlpatterns = [
    path('', WomenInSpotlight_list, name='WISList'),
    path('contact_us/', ContactUs_view, name='contact_us')
]