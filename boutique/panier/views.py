from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from produits.models import Produit
import json


class PanierDetailView(TemplateView):
    """Afficher le panier"""
    template_name = 'panier_detail.html'
    
    def get_context_data(self, **kwargs):
        """Construire le contexte du panier"""
        context = super().get_context_data(**kwargs)
        
        panier = self.request.session.get('panier', {})
        produits_panier = []
        total = 0
        
        for produit_id, quantite in panier.items():
            try:
                produit = Produit.objects.get(id=produit_id)
                sous_total = produit.prix * quantite
                produits_panier.append({
                    'produit': produit,
                    'quantite': quantite,
                    'sous_total': sous_total
                })
                total += sous_total
            except Produit.DoesNotExist:
                continue
        
        context.update({
            'produits_panier': produits_panier,
            'total': total,
            'nombre_articles': sum(panier.values())
        })
        return context


class AjouterAuPanierView(View):
    """Ajouter un produit au panier via AJAX"""
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, produit_id):
        produit = get_object_or_404(Produit, id=produit_id)
        
        if not produit.est_disponible:
            return JsonResponse({
                'success': False,
                'message': f'{produit.nom} n\'est pas disponible.'
            })
        
        # Récupérer ou initialiser le panier
        panier = request.session.get('panier', {})
        produit_id_str = str(produit_id)
        
        # Ajouter/incrémenter la quantité
        if produit_id_str in panier:
            panier[produit_id_str] += 1
        else:
            panier[produit_id_str] = 1
        
        # Vérifier le stock
        if panier[produit_id_str] > produit.stock:
            return JsonResponse({
                'success': False,
                'message': f'Stock insuffisant. Disponible: {produit.stock}'
            })
        
        # Sauvegarder en session
        request.session['panier'] = panier
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': f'{produit.nom} ajouté au panier !',
            'nombre_articles': sum(panier.values())
        })


class SupprimerDuPanierView(View):
    """Supprimer un produit du panier"""
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, produit_id):
        panier = request.session.get('panier', {})
        produit_id_str = str(produit_id)
        
        if produit_id_str in panier:
            produit = get_object_or_404(Produit, id=produit_id)
            del panier[produit_id_str]
            request.session['panier'] = panier
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': f'{produit.nom} supprimé du panier.',
                'nombre_articles': sum(panier.values())
            })
        
        return JsonResponse({
            'success': False,
            'message': 'Produit non trouvé dans le panier.'
        })


class ViderPanierView(View):
    """Vider complètement le panier"""
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        request.session['panier'] = {}
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Panier vidé avec succès.',
            'nombre_articles': 0
        })
