from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Produit, Categorie


class AccueilView(ListView):
    """Page d'accueil avec liste des produits et filtrage par catégorie"""
    model = Produit
    template_name = 'accueil.html'
    context_object_name = 'produits'
    
    def get_queryset(self):
        """Filtrer les produits par catégorie si spécifiée"""
        categorie_id = self.request.GET.get('categorie')
        
        if categorie_id and categorie_id != 'all':
            try:
                return Produit.objects.filter(categorie_id=categorie_id)
            except ValueError:
                return Produit.objects.all()
        return Produit.objects.all()
    
    def get_context_data(self, **kwargs):
        """Ajouter les catégories et statistiques au contexte"""
        context = super().get_context_data(**kwargs)
        
        # Catégories avec compteur de produits
        categories = Categorie.objects.annotate(
            count=Count('produit')
        )
        
        context.update({
            'categories': categories,
            'categories_with_count': [
                {'categorie': cat, 'count': cat.count} 
                for cat in categories
            ],
            'categorie_selectionnee': self.request.GET.get('categorie'),
            'total_produits': Produit.objects.count(),
        })
        return context


class ProduitDetailView(DetailView):
    """Page de détail d'un produit"""
    model = Produit
    template_name = 'produit_detail.html'
    context_object_name = 'produit'
    pk_url_kwarg = 'produit_id'
    
    def get_context_data(self, **kwargs):
        """Ajouter les produits similaires au contexte"""
        context = super().get_context_data(**kwargs)
        
        # Produits similaires de la même catégorie
        produits_similaires = Produit.objects.filter(
            categorie=self.object.categorie
        ).exclude(id=self.object.id)[:4]
        
        context['produits_similaires'] = produits_similaires
        return context

