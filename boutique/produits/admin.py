from django.contrib import admin
from .models import Categorie, Produit


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom', 'description')
    list_filter = ('date_creation',)
    readonly_fields = ('date_creation',)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'categorie', 'stock', 'disponible', 'date_creation')
    list_filter = ('categorie', 'disponible', 'date_creation')
    search_fields = ('nom', 'description')
    list_editable = ('prix', 'stock', 'disponible')
    readonly_fields = ('date_creation',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'categorie')
        }),
        ('Prix et stock', {
            'fields': ('prix', 'stock', 'disponible')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        })
    )
