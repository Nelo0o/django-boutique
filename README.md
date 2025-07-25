# Django Boutique

Projet de cours - Boutique en ligne avec Django et PostgreSQL.

## Fonctionnalités

**Clients :**
- Authentification (inscription, connexion)
- Catalogue produits avec filtrage par catégorie
- Panier d'achats (AJAX)
- Validation de commandes
- Historique des achats

**Administrateurs :**
- Dashboard avec statistiques (CA total, commandes validées)
- Gestion produits/catégories via Django Admin
- Export CSV des commandes du jour
- Notifications automatiques

## Installation

### Avec Docker (recommandé)

```bash
# Cloner le projet
git clone <repo-url>
cd django-boutique

# Configuration
cp .env.example .env
# Éditer .env si nécessaire

# Lancer
docker-compose up --build
```

**Accès :**
- Application : http://localhost:8000
- Admin : http://localhost:8000/admin
- Dashboard : http://localhost:8000/admin/dashboard
- API CSV : http://localhost:8000/api/commandes/csv

### Données de test

```bash
docker-compose exec web python populate_db.py
```

## Structure

```
boutique/
├── api/              # API CSV
├── commandes/        # Gestion commandes
├── comptes/          # Authentification
├── dashboard/        # Dashboard admin
├── panier/           # Panier d'achats
├── produits/         # Catalogue
└── notifications/    # Système notifications
```

## Technologies

- Django 5.2.4
- PostgreSQL
- Docker
- Tailwind CSS
- AJAX

## Commandes utiles

```bash
# Migrations
docker-compose exec web python manage.py migrate

# Superutilisateur
docker-compose exec web python manage.py createsuperuser

# Logs
docker-compose logs -f

# Arrêter
docker-compose down
```