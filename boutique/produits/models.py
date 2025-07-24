from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='produits/')
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(
        default=True, 
        help_text="Décochez pour rendre le produit indisponible même s'il y a du stock"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.nom
    
    @property
    def est_disponible(self):
        return self.stock > 0 and self.disponible
    
    @property
    def statut_stock(self):
        if not self.disponible:
            return "Indisponible"
        elif self.stock == 0:
            return "Épuisé"
        elif self.stock <= 5:
            return f"Stock faible ({self.stock})"
        else:
            return f"En stock ({self.stock})"