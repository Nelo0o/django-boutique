from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Produit


@receiver(pre_save, sender=Produit)
def check_produit_disponible(sender, instance, **kwargs):
    if instance.stock == 0:
        instance.disponible = False
    else:
        instance.disponible = True
