from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.DashboardAdminView.as_view(), name='admin'),
]
