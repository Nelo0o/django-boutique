from django.contrib import admin
from .models import Commande, ArticleCommande


class ArticleCommandeInline(admin.TabularInline):
    model = ArticleCommande
    extra = 0
    readonly_fields = ('prix_total',)


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'statut', 'prix_total', 'nombre_articles', 'date_creation')
    list_filter = ('statut', 'date_creation')
    search_fields = ('utilisateur__username', 'utilisateur__email')
    readonly_fields = ('date_creation', 'date_modification', 'nombre_articles')
    list_editable = ('statut',)
    inlines = [ArticleCommandeInline]
    
    fieldsets = (
        ('Informations commande', {
            'fields': ('utilisateur', 'statut', 'prix_total')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        })
    )


@admin.register(ArticleCommande)
class ArticleCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'prix_unitaire', 'prix_total')
    list_filter = ('commande__statut', 'commande__date_creation')
    search_fields = ('commande__utilisateur__username', 'produit__nom')
    readonly_fields = ('prix_total',)
