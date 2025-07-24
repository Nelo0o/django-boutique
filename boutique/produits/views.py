from django.shortcuts import render, get_object_or_404
from .models import Produit, Categorie


def accueil(request):
    """Page d'accueil avec liste des produits et filtrage par catégorie"""
    categorie_id = request.GET.get('categorie')
    
    if categorie_id and categorie_id != 'all':
        try:
            produits = Produit.objects.filter(categorie_id=categorie_id)
        except ValueError:
            produits = Produit.objects.all()
    else:
        produits = Produit.objects.all()
    
    categories = Categorie.objects.all()
    
    categories_with_count = []
    for categorie in categories:
        count = Produit.objects.filter(categorie=categorie).count()
        categories_with_count.append({
            'categorie': categorie,
            'count': count
        })
    
    context = {
        'produits': produits,
        'categories': categories,
        'categories_with_count': categories_with_count,
        'categorie_selectionnee': categorie_id,
        'total_produits': Produit.objects.count(),
    }
    return render(request, 'accueil.html', context)


def produit_detail(request, produit_id):
    """Page de détail d'un produit"""
    produit = get_object_or_404(Produit, id=produit_id)
    
    produits_similaires = Produit.objects.filter(
        categorie=produit.categorie
    ).exclude(id=produit.id)[:4]
    
    context = {
        'produit': produit,
        'produits_similaires': produits_similaires,
    }
    return render(request, 'produit_detail.html', context)

