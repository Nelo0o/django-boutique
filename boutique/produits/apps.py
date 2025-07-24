from django.apps import AppConfig


class ProduitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produits'
    
    def ready(self):
        """Importer les signals quand l'app est prête"""
        import produits.signals
