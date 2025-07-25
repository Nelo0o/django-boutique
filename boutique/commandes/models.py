from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from produits.models import Produit


class CommandeQuerySet(models.QuerySet):
    """QuerySet personnalisé pour les commandes avec méthodes optimisées"""
    
    def validees(self):
        """Retourne uniquement les commandes payées"""
        return self.filter(statut='payee')
    
    def avec_details(self):
        """Optimise les requêtes avec select_related"""
        return self.select_related('utilisateur')
    
    def ca_total(self):
        """Calcule le CA total des commandes"""
        return self.aggregate(total=Sum('prix_total'))['total'] or 0
    
    def statistiques_dashboard(self):
        """Retourne les statistiques pour le dashboard"""
        return self.aggregate(
            ca_total=Sum('prix_total'),
            nombre_commandes=Count('id')
        )
    
    def par_periode(self, jours=30):
        """Filtre les commandes sur une période donnée"""
        from django.utils import timezone
        from datetime import timedelta
        date_limite = timezone.now() - timedelta(days=jours)
        return self.filter(date_creation__gte=date_limite)


class CommandeManager(models.Manager):
    """Manager personnalisé pour les commandes avec méthodes optimisées"""
    
    def get_queryset(self):
        """Retourne le QuerySet personnalisé"""
        return CommandeQuerySet(self.model, using=self._db)
    
    def validees(self):
        """Raccourci pour les commandes validées"""
        return self.get_queryset().validees()
    
    def avec_details(self):
        """Raccourci pour les requêtes optimisées"""
        return self.get_queryset().avec_details()
    
    def dashboard_stats(self):
        """Statistiques complètes pour le dashboard admin"""
        return self.validees().avec_details().statistiques_dashboard()
    
    def ca_total(self):
        """CA total de toutes les commandes validées"""
        return self.validees().ca_total()
    
    def commandes_recentes(self, limit=10):
        """Dernières commandes validées pour le dashboard"""
        return self.validees().avec_details().order_by('-date_creation')[:limit]


class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Commande #{self.id} - {self.utilisateur.username}"

    def nombre_articles(self):
        return sum(item.quantite for item in self.articles.all())
    
    
    objects = CommandeManager()


class ArticleCommandeQuerySet(models.QuerySet):
    """QuerySet personnalisé pour les articles de commande"""
    
    def produits_populaires(self):
        """Retourne les produits les plus vendus"""
        return self.values('produit__nom', 'produit__id').annotate(
            total_vendu=Sum('quantite')
        ).order_by('-total_vendu')
    
    def ca_par_produit(self):
        """Calcule le CA par produit"""
        return self.values('produit__nom').annotate(
            ca_produit=Sum(models.F('quantite') * models.F('prix_unitaire'))
        ).order_by('-ca_produit')


class ArticleCommandeManager(models.Manager):
    """Manager personnalisé pour les articles de commande"""
    
    def get_queryset(self):
        """Retourne le QuerySet personnalisé"""
        return ArticleCommandeQuerySet(self.model, using=self._db)
    
    def produits_populaires(self, limit=5):
        """Top des produits les plus vendus"""
        return self.get_queryset().produits_populaires()[:limit]
    
    def ca_par_produit(self, limit=5):
        """CA par produit pour le dashboard"""
        return self.get_queryset().ca_par_produit()[:limit]


class ArticleCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='articles', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    def prix_total(self):
        return self.quantite * self.prix_unitaire
    

    objects = ArticleCommandeManager()
