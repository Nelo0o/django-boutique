from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('commandes/csv/', views.CommandesCSVView.as_view(), name='commandes_csv'),
]
