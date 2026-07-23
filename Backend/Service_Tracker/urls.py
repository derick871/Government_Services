from django.urls import path
from .models import views

urlpatterns= [
    # Aggregate Data Endpoint
    path('notices/', views.CountyNoticeListView.as_view(), name='notice-list'),
    path('notices/county/<str:county_id>/', views.CountyNoticeByCountyView.as_view(), name='notice-by-county'),
    # Citizen Application Tracking Endpoints
    path('applications/', views.ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/track/<str:tracking_number>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    
    # Administrative FSM Status Update Pipeline
    path('applications/<int:pk>/transition/', views.UpdateApplicationStatusView.as_view(), name='application-transition'),
]