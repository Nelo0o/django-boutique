from django.contrib import admin
from .models import Panier, ArticlePanier


class ArticlePanierInline(admin.TabularInline):
    model = ArticlePanier
    extra = 0
    readonly_fields = ('date_ajout',)


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'nombre_articles', 'prix_total', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('utilisateur__username', 'utilisateur__email')
    readonly_fields = ('date_creation', 'date_modification', 'prix_total', 'nombre_articles')
    inlines = [ArticlePanierInline]


@admin.register(ArticlePanier)
class ArticlePanierAdmin(admin.ModelAdmin):
    list_display = ('panier', 'produit', 'quantite', 'prix_total', 'date_ajout')
    list_filter = ('date_ajout', 'produit__categorie')
    search_fields = ('panier__utilisateur__username', 'produit__nom')
    readonly_fields = ('date_ajout', 'prix_total')
