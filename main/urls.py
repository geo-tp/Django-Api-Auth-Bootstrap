from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# from user.views import UserViewSet
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from django.conf.urls.static import static
import main.settings as settings

admin.site.site_header = "API Administration"
admin.site.site_title = "API Administration"
admin.site.index_title = "Database models from API"

api_router = routers.DefaultRouter()
# api_router.register(r"model", ModelViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/", include((api_router.urls))),
    path(
        "api/v1/endpoints/",
        include_docs_urls(
            title="API V1 Endpoints",
            permission_classes=[permissions.AllowAny],
        ),
    ),
]

# if settings.DEBUG is True:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
