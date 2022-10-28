from django.urls import path
from rest_framework.authtoken import views as auth_views
from .views import (
    login,
    logout,
    register,
    email_validation,
    password_update,
    password_forget,
    password_reset,
)

urlpatterns = [
    path("login", login, name="api_login"),
    path("logout", logout, name="api_logout"),
    path("register", register, name="api_register"),
    path("email-validation/<key>", email_validation, name="api_email_validation"),
    path("password-update", password_update, name="api_password_update"),
    path("password-forget", password_forget, name="api_password_forget"),
]
