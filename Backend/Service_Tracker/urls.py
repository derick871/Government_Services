from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = "Service_Tracker"

urlpatterns = [
    # ==========================
    # Authentication Endpoints
    # ==========================
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # ==========================
    # County Notices
    # ==========================
    path(
        "notices/",
        views.CountyNoticeListView.as_view(),  # Fixed: View class uncommented so path is valid
        name="notice-list",
    ),
    path(
        "notices/county/<str:county_id>/",
        views.CountyNoticeByCountyView.as_view(),
        name="notice-by-county",
    ),

    # ==========================
    # Applications
    # ==========================
    path(
        "applications/",
        views.ApplicationListCreateView.as_view(),
        name="application-list-create",
    ),
    path(
        "applications/track/<str:tracking_number>/",
        views.ApplicationDetailView.as_view(),
        name="application-detail",
    ),
    path(
        "applications/<int:pk>/transition/",
        views.UpdateApplicationStatusView.as_view(),
        name="application-transition",
    ),
]