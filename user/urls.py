from django.urls import path
from .views import profile_view, password_view, image_view

urlpatterns = [
    path("profile", profile_view, name="api_user_profile"),
    path("password", password_view, name="api_user_password"),
    path("image", image_view, name="api_user_image"),
]
