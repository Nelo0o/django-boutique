#!/usr/bin/env python

# Script pour populer la base de données pour les différentes tables

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique.settings')
django.setup()

from produits.models import Categorie, Produit

def create_categories():
    """Créer les catégories streetwear"""
    categories_data = [
        {
            'nom': 'T-Shirts',
            'description': 'T-shirts streetwear premium avec designs exclusifs'
        },
        {
            'nom': 'Hoodies',
            'description': 'Sweats à capuche urbains de qualité supérieure'
        },
        {
            'nom': 'Sneakers',
            'description': 'Baskets streetwear et éditions limitées'
        },
        {
            'nom': 'Casquettes',
            'description': 'Casquettes et bonnets style urbain'
        },
        {
            'nom': 'Jeans',
            'description': 'Denim streetwear et pantalons urbains'
        },
        {
            'nom': 'Vestes',
            'description': 'Vestes bomber, coach et streetwear'
        },
        {
            'nom': 'Accessoires',
            'description': 'Sacs, bijoux et accessoires streetwear'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Categorie.objects.get_or_create(
            nom=cat_data['nom'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['nom']] = category
        if created:
            print(f"✅ Catégorie créée: {category.nom}")
        else:
            print(f"⚠️  Catégorie existe déjà: {category.nom}")
    
    return categories

def create_products(categories):
    """Créer les produits streetwear"""
    products_data = [
        # T-Shirts
        {
            'nom': 'URBAN LEGEND TEE',
            'description': 'T-shirt premium en coton bio avec print exclusif. Coupe oversize pour un style authentique streetwear.',
            'prix': 45.00,
            'categorie': 'T-Shirts',
            'stock': 25,
            'disponible': True
        },
        {
            'nom': 'MIDNIGHT VIBES TEE',
            'description': 'Design minimaliste noir sur blanc. Parfait pour un look urbain décontracté.',
            'prix': 39.90,
            'categorie': 'T-Shirts',
            'stock': 30,
            'disponible': True
        },
        {
            'nom': 'STREET KING TEE',
            'description': 'T-shirt graphique avec typography bold. Edition limitée pour les vrais connaisseurs.',
            'prix': 52.00,
            'categorie': 'T-Shirts',
            'stock': 15,
            'disponible': True
        },
        
        # Hoodies
        {
            'nom': 'SHADOW HOODIE',
            'description': 'Hoodie premium avec capuche doublée. Matière épaisse et chaude pour l\'hiver urbain.',
            'prix': 89.90,
            'categorie': 'Hoodies',
            'stock': 20,
            'disponible': True
        },
        {
            'nom': 'NEON NIGHTS HOODIE',
            'description': 'Design fluorescent qui brille dans le noir. Style unique pour se démarquer.',
            'prix': 95.00,
            'categorie': 'Hoodies',
            'stock': 12,
            'disponible': True
        },
        {
            'nom': 'MINIMAL HOODIE',
            'description': 'Hoodie épuré sans logo apparent. Pour ceux qui préfèrent la discrétion.',
            'prix': 79.90,
            'categorie': 'Hoodies',
            'stock': 0,
            'disponible': False
        },
        
        # Sneakers
        {
            'nom': 'GHOST RUNNER',
            'description': 'Sneakers blanches minimalistes. Confort maximal et style intemporel.',
            'prix': 129.90,
            'categorie': 'Sneakers',
            'stock': 18,
            'disponible': True
        },
        {
            'nom': 'NIGHT WALKER',
            'description': 'Baskets noires avec détails réfléchissants. Parfaites pour les sorties nocturnes.',
            'prix': 149.90,
            'categorie': 'Sneakers',
            'stock': 8,
            'disponible': True
        },
        {
            'nom': 'RETRO VIBES',
            'description': 'Sneakers vintage remises au goût du jour. Style rétro avec technologies modernes.',
            'prix': 139.90,
            'categorie': 'Sneakers',
            'stock': 22,
            'disponible': True
        },
        
        # Casquettes
        {
            'nom': 'URBAN CAP',
            'description': 'Casquette snapback avec broderie 3D. Ajustable et style authentique.',
            'prix': 29.90,
            'categorie': 'Casquettes',
            'stock': 35,
            'disponible': True
        },
        {
            'nom': 'STEALTH BEANIE',
            'description': 'Bonnet noir minimaliste. Parfait pour les looks urbains discrets.',
            'prix': 24.90,
            'categorie': 'Casquettes',
            'stock': 40,
            'disponible': True
        },
        
        # Jeans
        {
            'nom': 'DISTRESSED DENIM',
            'description': 'Jean déchiré avec finitions artisanales. Style grunge moderne.',
            'prix': 89.90,
            'categorie': 'Jeans',
            'stock': 16,
            'disponible': True
        },
        {
            'nom': 'SLIM BLACK JEANS',
            'description': 'Jean noir coupe slim. Basique indispensable du dressing streetwear.',
            'prix': 69.90,
            'categorie': 'Jeans',
            'stock': 28,
            'disponible': True
        },
        
        # Vestes
        {
            'nom': 'BOMBER JACKET',
            'description': 'Veste bomber classique revisitée. Matière technique et coupe moderne.',
            'prix': 119.90,
            'categorie': 'Vestes',
            'stock': 14,
            'disponible': True
        },
        {
            'nom': 'COACH JACKET',
            'description': 'Veste coach imperméable. Parfaite pour les mi-saisons urbaines.',
            'prix': 99.90,
            'categorie': 'Vestes',
            'stock': 0,
            'disponible': False
        },
        
        # Accessoires
        {
            'nom': 'STREET BAG',
            'description': 'Sac bandoulière technique. Compartiments multiples pour l\'urbain moderne.',
            'prix': 59.90,
            'categorie': 'Accessoires',
            'stock': 25,
            'disponible': True
        },
        {
            'nom': 'CHAIN NECKLACE',
            'description': 'Chaîne en acier inoxydable. Accessoire indispensable du style streetwear.',
            'prix': 34.90,
            'categorie': 'Accessoires',
            'stock': 50,
            'disponible': True
        }
    ]
    
    for product_data in products_data:
        category = categories[product_data['categorie']]
        
        product, created = Produit.objects.get_or_create(
            nom=product_data['nom'],
            defaults={
                'description': product_data['description'],
                'prix': product_data['prix'],
                'categorie': category,
                'stock': product_data['stock'],
                'disponible': product_data['disponible']
            }
        )
        
        if created:
            print(f"✅ Produit créé: {product.nom} - {product.prix}€")
        else:
            print(f"⚠️  Produit existe déjà: {product.nom}")

def main():
    """Fonction principale"""
    print("🚀 Début de la population de la base de données streetwear...")
    print()
    
    # Créer les catégories
    print("📁 Création des catégories...")
    categories = create_categories()
    print()
    
    # Créer les produits
    print("👕 Création des produits...")
    create_products(categories)
    print()
    
    print("✨ Population terminée !")
    print(f"📊 Résumé:")
    print(f"   - Catégories: {Categorie.objects.count()}")
    print(f"   - Produits: {Produit.objects.count()}")
    print(f"   - Produits disponibles: {Produit.objects.filter(disponible=True).count()}")

if __name__ == '__main__':
    main()
