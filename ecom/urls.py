# ecom/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import user_login  # Import the user_login view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Ensure 'store.urls' is correct
    path('login/', user_login, name='login'),  # Add the login URL
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

