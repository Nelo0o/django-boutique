from django.db.models.signals import post_save
from django.dispatch import receiver
from commandes.models import Commande
from .models import Notification


@receiver(post_save, sender=Commande)
def creer_notification_nouvelle_commande(sender, instance, created, **kwargs):
    """Créer une notification quand une nouvelle commande est créée"""
    if created and instance.statut == 'payee':
        Notification.objects.create(
            type='nouvelle_commande',
            titre=f'Nouvelle commande #{instance.id}',
            message=f'Commande de {instance.prix_total}€ passée par {instance.utilisateur.username}',
            commande=instance
        )
