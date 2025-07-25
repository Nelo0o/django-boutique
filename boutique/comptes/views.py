from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from commandes.models import Commande


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée"""
    template_name = 'compte_connexion.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Rediriger vers la page d'accueil après connexion"""
        return reverse_lazy('produits:accueil')
    
    def form_valid(self, form):
        """Message de succès à la connexion"""
        messages.success(self.request, f'Bienvenue {form.get_user().username} !')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Vue de déconnexion personnalisée"""
    http_method_names = ['get', 'post']
    
    def post(self, request, *args, **kwargs):
        """Traiter la déconnexion POST"""
        if request.user.is_authenticated:
            messages.success(request, 'Vous avez été déconnecté avec succès.')
        response = super().post(request, *args, **kwargs)
        return redirect('produits:accueil')
    
    def get(self, request, *args, **kwargs):
        """Traiter la déconnexion GET"""
        if request.user.is_authenticated:
            messages.success(request, 'Vous avez été déconnecté avec succès.')
        response = super().get(request, *args, **kwargs)
        return redirect('produits:accueil')


class InscriptionView(CreateView):
    """Vue d'inscription des nouveaux utilisateurs"""
    form_class = UserCreationForm
    template_name = 'compte_inscription.html'
    success_url = reverse_lazy('comptes:login')
    
    def form_valid(self, form):
        """Message de succès à l'inscription"""
        messages.success(
            self.request, 
            'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.'
        )
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        """Rediriger les utilisateurs déjà connectés"""
        if request.user.is_authenticated:
            return redirect('produits:accueil')
        return super().dispatch(request, *args, **kwargs)


class CompteClientView(LoginRequiredMixin, TemplateView):
    """Page du compte client avec historique des commandes"""
    template_name = 'compte_client.html'
    login_url = 'comptes:login'
    
    def get_context_data(self, **kwargs):
        """Ajouter les commandes de l'utilisateur au contexte"""
        context = super().get_context_data(**kwargs)
        
        # Récupérer les commandes de l'utilisateur
        commandes = Commande.objects.filter(
            utilisateur=self.request.user
        ).order_by('-date_creation')
        
        # Statistiques utilisateur
        total_commandes = commandes.count()
        total_depense = sum(cmd.prix_total for cmd in commandes)
        commandes_payees = commandes.filter(statut='payee').count()
        
        context.update({
            'commandes': commandes,
            'total_commandes': total_commandes,
            'total_depense': total_depense,
            'commandes_payees': commandes_payees,
        })
        return context
