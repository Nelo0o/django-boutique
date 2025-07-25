from django.urls import path
from . import views

app_name = 'panier'

urlpatterns = [
    path('', views.PanierDetailView.as_view(), name='detail'),
    path('ajouter/<int:produit_id>/', views.AjouterAuPanierView.as_view(), name='ajouter'),
    path('supprimer/<int:produit_id>/', views.SupprimerDuPanierView.as_view(), name='supprimer'),
    path('vider/', views.ViderPanierView.as_view(), name='vider'),
    path('commander/', views.CommanderView.as_view(), name='commander'),
]
