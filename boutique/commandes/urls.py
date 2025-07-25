from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    path('commander/', views.CommanderView.as_view(), name='commander'),
]
