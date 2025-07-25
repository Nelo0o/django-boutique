from django.apps import AppConfig


class CommandesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commandes'
    
    def ready(self):
        """Importer les signals quand l'app est prête"""
        import commandes.signals
