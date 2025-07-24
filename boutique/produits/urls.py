from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('produit/<int:produit_id>/', views.produit_detail, name='produit_detail'),
]
