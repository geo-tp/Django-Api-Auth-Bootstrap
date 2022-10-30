from django.urls import path
from .views import (
    login,
    logout,
    register,
    email_validation,
    password_forget,
    password_reset,
    deactivate_account,
)

urlpatterns = [
    path("login", login, name="api_login"),
    path("logout", logout, name="api_logout"),
    path("register", register, name="api_register"),
    path("email-validation/<key>", email_validation, name="api_email_validation"),
    path("password-forget", password_forget, name="api_password_forget"),
    path("password-reset/<key>", password_reset, name="api_password_reset"),
    path("deactivate-account", deactivate_account,
         name="api_deactivate_account"),
]
