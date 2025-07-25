from django.urls import path
from . import views

app_name = 'panier'

urlpatterns = [
    path('', views.panier_detail, name='detail'),
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter'),
    path('supprimer/<int:produit_id>/', views.supprimer_du_panier, name='supprimer'),
    path('vider/', views.vider_panier, name='vider'),
]
