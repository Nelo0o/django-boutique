import csv
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import messages
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
    
    def get_urls(self):
        """Ajouter l'URL pour le bouton CSV"""
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv), name='commandes_export_csv'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        """Ajouter le bouton CSV"""
        extra_context = extra_context or {}
        extra_context['csv_url'] = reverse('admin:commandes_export_csv')
        return super().changelist_view(request, extra_context=extra_context)
    
    def export_csv(self, request):
        """Utiliser l'API pour exporter"""
        from api.views import CommandesCSVView
        return CommandesCSVView().get(request)


@admin.register(ArticleCommande)
class ArticleCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'prix_unitaire', 'prix_total')
    list_filter = ('commande__statut', 'commande__date_creation')
    search_fields = ('commande__utilisateur__username', 'produit__nom')
    readonly_fields = ('prix_total',)
