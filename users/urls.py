from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # Map login view to the URL
    # Add other user-related URLs here if needed
]
