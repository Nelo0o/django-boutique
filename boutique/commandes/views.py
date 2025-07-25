from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from .models import Commande, ArticleCommande
from produits.models import Produit


class CommanderView(LoginRequiredMixin, View):
    """Vue pour convertir le panier en commande payée"""
    login_url = 'comptes:login'
    
    def post(self, request):
        """Traiter la commande du panier"""
        panier = request.session.get('panier', {})
        
        # Vérifier que le panier n'est pas vide
        if not panier:
            messages.error(request, 'Votre panier est vide.')
            return redirect('panier:detail')
        
        # Préparer les données de commande
        articles_commande = []
        total = 0
        
        # Vérifier la disponibilité et calculer le total
        for produit_id, quantite in panier.items():
            try:
                produit = Produit.objects.get(id=produit_id)
                
                # Vérifier la disponibilité
                if not produit.disponible:
                    messages.error(request, f'Le produit "{produit.nom}" n\'est plus disponible.')
                    return redirect('panier:detail')
                
                # Vérifier le stock 
                if produit.stock < quantite:
                    messages.error(request, f'Stock insuffisant pour "{produit.nom}". Stock disponible: {produit.stock}')
                    return redirect('panier:detail')
                
                # Calculer le prix
                prix_unitaire = produit.prix
                sous_total = prix_unitaire * quantite
                total += sous_total
                
                articles_commande.append({
                    'produit': produit,
                    'quantite': quantite,
                    'prix_unitaire': prix_unitaire
                })
                
            except Produit.DoesNotExist:
                messages.error(request, 'Un produit de votre panier n\'existe plus.')
                return redirect('panier:detail')
        
        try:
            with transaction.atomic():
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
            messages.error(request, f'Erreur lors de la création de la commande: {str(e)}')
            return redirect('panier:detail')
