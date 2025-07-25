from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from .models import Commande
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Commande)
def commande_validee_notification(sender, instance, created, **kwargs):
    """
    Signal déclenché à la validation d'une commande.
    Envoie une notification aux super_users.
    """
    # Vérifier si c'est une nouvelle commande payée
    if created and instance.statut == 'payee':
        # Log de la nouvelle commande
        logger.info(f"Nouvelle commande validée: #{instance.id} - {instance.utilisateur.username} - {instance.prix_total}€")
        
        # Message de notification (visible dans l'admin)
        notification_message = (
            f"🎉 NOUVELLE COMMANDE VALIDÉE!\n"
            f"Commande #{instance.id}\n"
            f"Client: {instance.utilisateur.username}\n"
            f"Montant: {instance.prix_total}€\n"
            f"Articles: {instance.nombre_articles()}\n"
            f"Date: {instance.date_creation.strftime('%d/%m/%Y %H:%M')}"
        )
        
        # Afficher dans la console pour les super_users
        print("=" * 50)
        print("🚨 NOTIFICATION ADMIN - NOUVELLE COMMANDE")
        print("=" * 50)
        print(notification_message)
        print("=" * 50)
        
        # Optionnel: Envoyer un email aux super_users
        try:
            # Récupérer tous les super_users
            from django.contrib.auth.models import User
            super_users = User.objects.filter(is_superuser=True)
            
            if super_users.exists():
                admin_emails = [user.email for user in super_users if user.email]
                
                if admin_emails:
                    send_mail(
                        subject=f'Nouvelle commande #{instance.id} - RABIBS',
                        message=notification_message,
                        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@rabibs.com',
                        recipient_list=admin_emails,
                        fail_silently=True,  # Ne pas faire planter si l'email échoue
                    )
                    logger.info(f"Email de notification envoyé à {len(admin_emails)} admin(s)")
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de notification: {e}")
    
    # Notification pour changement de statut
    elif not created and instance.statut == 'payee':
        logger.info(f"Commande #{instance.id} mise à jour vers statut 'payée'")


@receiver(post_save, sender=Commande)
def mise_a_jour_ca_total(sender, instance, created, **kwargs):
    """
    Signal pour mettre à jour les statistiques de CA.
    Peut être utilisé pour des calculs en temps réel.
    """
    if instance.statut == 'payee':
        # Calculer le CA total des commandes payées
        ca_total = Commande.objects.filter(statut='payee').aggregate(
            total=models.Sum('prix_total')
        )['total'] or 0
        
        logger.info(f"CA total mis à jour: {ca_total}€")
        
        # Afficher le CA dans la console pour les admins
        if created:
            print(f"💰 CA TOTAL ACTUEL: {ca_total}€")
