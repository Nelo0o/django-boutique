from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.AccueilView.as_view(), name='accueil'),
    path('produit/<int:produit_id>/', views.ProduitDetailView.as_view(), name='produit_detail'),
]
