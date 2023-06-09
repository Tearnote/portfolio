from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('allauth.urls')),
    path('projects/', include('projects.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('userprofile.urls')),
    path('', include('home.urls')),
]
