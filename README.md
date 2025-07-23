# Django Boutique

Une application Django dockerisée avec PostgreSQL.

## 🚀 Démarrage rapide avec Docker

### Prérequis
- Docker
- Docker Compose

### Installation et lancement

1. **Cloner le projet**
   ```bash
   git clone <votre-repo>
   cd django-boutique
   ```

2. **Construire et lancer les conteneurs**
   ```bash
   docker-compose up --build
   ```

3. **Accéder à l'application**
   - Application : http://localhost:8000
   - Admin Django : http://localhost:8000/admin

### 🔐 Personnaliser la configuration

**Méthode recommandée** : Créez un fichier `.env` à partir du template :

```bash
cp .env.example .env
```

Puis modifiez les valeurs dans `.env` selon vos besoins :

```bash
# Superutilisateur Django
DJANGO_SUPERUSER_USERNAME=mon_admin
DJANGO_SUPERUSER_EMAIL=mon_email@example.com
DJANGO_SUPERUSER_PASSWORD=mon_mot_de_passe_securise

# Base de données
DB_NAME=ma_boutique
DB_USER=mon_user
DB_PASSWORD=mon_password
```

### Commandes utiles

```bash
# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les conteneurs
docker-compose down

# Supprimer les volumes (attention: supprime les données)
docker-compose down -v

# Exécuter des commandes Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

## 🗄️ Base de données

- **Type** : PostgreSQL 15
- **Nom** : boutique_db
- **Utilisateur** : boutique_user
- **Port** : 5432

## 📁 Structure du projet

```
django-boutique/
├── boutique/              # Code Django
│   ├── boutique/         # Configuration Django
│   └── manage.py
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Orchestration des services
├── requirements.txt      # Dépendances Python
├── .env                 # Variables d'environnement
└── init.sh              # Script d'initialisation
```

## 🛠️ Développement

Pour le développement local, vous pouvez modifier les fichiers directement. Les changements sont automatiquement synchronisés grâce au volume monté.

## 🔧 Configuration

Les variables d'environnement sont définies dans le fichier `.env`. Vous pouvez les modifier selon vos besoins. Django