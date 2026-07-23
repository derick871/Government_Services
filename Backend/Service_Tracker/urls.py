from django.urls import path
from .models import views

urlpatterns= [
    # Aggregate Data Endpoint
    path('notices/', views.CountyNoticeListView.as_view(), name='notice-list'),
    path('notices/county/<str:county_id>/', views.CountyNoticeByCountyView.as_view(), name='notice-by-county'),
]