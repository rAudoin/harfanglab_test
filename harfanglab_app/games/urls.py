from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from . import views

router = DefaultRouter()
router.register(r"games", views.GameViewSet)
router.register(r"platforms", views.PlatformViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    # OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
