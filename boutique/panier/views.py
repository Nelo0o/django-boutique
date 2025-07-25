from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from produits.models import Produit
from commandes.models import Commande, ArticleCommande
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


class CommanderView(LoginRequiredMixin, View):
    """Vue pour passer commande - convertit le panier en commande"""
    login_url = 'comptes:login'
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        # Vérifier que l'utilisateur est connecté
        if not request.user.is_authenticated:
            messages.error(request, 'Vous devez être connecté pour passer commande.')
            return redirect('comptes:login')
        
        # Récupérer le panier
        panier = request.session.get('panier', {})
        
        if not panier:
            messages.error(request, 'Votre panier est vide.')
            return redirect('panier:detail')
        
        # Calculer le total et vérifier la disponibilité
        total = 0
        articles_commande = []
        
        for produit_id, quantite in panier.items():
            try:
                produit = Produit.objects.get(id=produit_id)
                
                # Vérifier la disponibilité et le stock
                if not produit.est_disponible:
                    messages.error(request, f'{produit.nom} n\'est plus disponible.')
                    return redirect('panier:detail')
                
                if quantite > produit.stock:
                    messages.error(request, f'Stock insuffisant pour {produit.nom}. Disponible: {produit.stock}')
                    return redirect('panier:detail')
                
                # Calculer le sous-total
                sous_total = produit.prix * quantite
                total += sous_total
                
                # Préparer l'article de commande
                articles_commande.append({
                    'produit': produit,
                    'quantite': quantite,
                    'prix_unitaire': produit.prix,
                    'sous_total': sous_total
                })
                
            except Produit.DoesNotExist:
                messages.error(request, 'Un produit de votre panier n\'existe plus.')
                return redirect('panier:detail')
        
        try:
            # Créer la commande
            commande = Commande.objects.create(
                utilisateur=request.user,
                prix_total=total,
                statut='payee'
            )
            
            # Créer les articles de commande et mettre à jour le stock
            for item in articles_commande:
                ArticleCommande.objects.create(
                    commande=commande,
                    produit=item['produit'],
                    quantite=item['quantite'],
                    prix_unitaire=item['prix_unitaire']
                )
                
                # Mettre à jour le stock
                produit = item['produit']
                produit.stock -= item['quantite']
                produit.save()
            
            # Vider le panier
            request.session['panier'] = {}
            request.session.modified = True
            
            # Message de succès
            messages.success(
                request, 
                f'Commande #{commande.id} passée avec succès ! Total: {total}€'
            )
            
            # Rediriger vers le compte client
            return redirect('comptes:compte_client')
            
        except Exception as e:
            messages.error(request, 'Une erreur est survenue lors de la commande. Veuillez réessayer.')
            return redirect('panier:detail')
