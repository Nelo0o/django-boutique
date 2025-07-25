from django.db import models
from django.contrib.auth.models import User
from commandes.models import Commande


class Notification(models.Model):
    """Modèle pour les notifications admin"""
    
    TYPE_CHOICES = [
        ('nouvelle_commande', 'Nouvelle commande'),
        ('stock_faible', 'Stock faible'),
        ('info', 'Information'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, null=True, blank=True)
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.titre} - {self.get_type_display()}"
    
    def marquer_comme_lu(self):
        """Marquer la notification comme lue"""
        self.lu = True
        self.save()
