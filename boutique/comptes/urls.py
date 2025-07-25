from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('compte/', views.CompteClientView.as_view(), name='compte_client'),
]
