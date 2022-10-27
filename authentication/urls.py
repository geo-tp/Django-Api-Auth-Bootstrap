from django.urls import path
from rest_framework.authtoken import views as auth_views
from .views import login, logout, register

urlpatterns = [
    path('login', login, name='api_login'),
    path('logout', logout, name="api_logout"),
    path('register', register, name='api_register'),
]
