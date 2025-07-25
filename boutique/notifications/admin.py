from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type', 'lu', 'date_creation', 'commande']
    list_filter = ['type', 'lu', 'date_creation']
    search_fields = ['titre', 'message']
    readonly_fields = ['date_creation']
    list_editable = ['lu']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('commande')
