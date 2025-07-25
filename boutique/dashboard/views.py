from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from commandes.models import Commande, ArticleCommande
from produits.models import Produit, Categorie
from django.contrib.auth.models import User
from notifications.models import Notification


class DashboardAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Dashboard pour les super_users avec statistiques et commandes"""
    template_name = 'dashboard_admin.html'
    login_url = '/admin/login/'
    
    def test_func(self):
        """Vérifier que l'utilisateur est un super_user"""
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        """Gestion personnalisée quand l'utilisateur n'a pas les permissions"""
        if not self.request.user.is_authenticated:
            messages.info(self.request, 'Vous devez vous connecter en tant qu\'administrateur pour accéder au dashboard.')
            return redirect('/admin/login/')
        else:
            messages.error(self.request, 'Accès refusé. Vous devez être administrateur pour accéder au dashboard.')
            return redirect('produits:accueil')
    
    def get_context_data(self, **kwargs):
        """Construire le contexte avec les statistiques essentielles"""
        context = super().get_context_data(**kwargs)
        
        commandes_validees = Commande.objects.commandes_recentes(limit=20)
        
        ca_stats = Commande.objects.dashboard_stats()
        ca_total = ca_stats['ca_total'] or 0
        nombre_commandes_payees = ca_stats['nombre_commandes'] or 0
        
        notifications_non_lues = Notification.objects.filter(lu=False).order_by('-date_creation')[:5]
        
        context.update({
            'commandes_validees': commandes_validees,
            'ca_total': ca_total,
            'nombre_commandes_payees': nombre_commandes_payees,
            'notifications_non_lues': notifications_non_lues,
        })
        
        return context
