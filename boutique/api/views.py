import csv
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from commandes.models import Commande
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


@method_decorator(staff_member_required, name='dispatch')
class CommandesCSVView(View):
    """API simple pour exporter les commandes du jour en CSV"""
    
    def get(self, request):
        # Commandes du jour
        aujourd_hui = timezone.now().date()
        commandes = Commande.objects.filter(date_creation__date=aujourd_hui)
        
        # Réponse CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="commandes_{aujourd_hui}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Utilisateur', 'Statut', 'Prix Total', 'Date'])
        
        for commande in commandes:
            writer.writerow([
                commande.id,
                commande.utilisateur.username,
                commande.statut,
                commande.prix_total,
                commande.date_creation.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
