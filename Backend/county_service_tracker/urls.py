"""
Root URL Configuration for drf_project.

This module establishes the top-level routing architecture for the application,
segregating administrative boundaries, core API endpoints, authentication mechanisms, 
and automated OpenAPI documentation schema views.
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenRefreshView

# -----------------------------------------------------------------------------
# CORE ROUTING PATHS
# -----------------------------------------------------------------------------
ADMIN_URLS = [
    path("admin/", admin.site.urls),
]

AUTH_URLS = [
    # Custom token pair generation (Login)
    path("api/v1/auth/token/", TokenRefreshView.as_view(), name="token_obtain_pair"),
    # Standard JWT refresh endpoint
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

DOCUMENTATION_URLS = [
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="api_schema"),
    path(
        "api/v1/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="api_schema"),
        name="swagger_ui",
    ),
    path(
        "api/v1/docs/redoc/",
        SpectacularRedocView.as_view(url_name="api_schema"),
        name="redoc_ui",
    ),
]

APPLICATION_URLS = [
    path("api/v1/", include("Service_Tracker.urls")),
]

# -----------------------------------------------------------------------------
# MAIN URLPATTERNS REGISTRY
# -----------------------------------------------------------------------------
urlpatterns = (
    ADMIN_URLS 
    + AUTH_URLS 
    + DOCUMENTATION_URLS 
    + APPLICATION_URLS
)