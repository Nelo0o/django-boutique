from django.db import models
from django.contrib.auth.models import User
from produits.models import Produit


class Panier(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

    def prix_total(self):
        return sum(item.prix_total() for item in self.articles.all())

    def nombre_articles(self):
        return sum(item.quantite for item in self.articles.all())


class ArticlePanier(models.Model):
    panier = models.ForeignKey(Panier, related_name='articles', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ('panier', 'produit')

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    def prix_total(self):
        return self.quantite * self.produit.prix
