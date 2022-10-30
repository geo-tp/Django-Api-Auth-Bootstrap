from django.urls import path
from .views import profile, password

urlpatterns = [
    path("profile", profile, name="api_user_profile"),
    path("password", password, name="api_user_password")

]
