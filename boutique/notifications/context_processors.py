from .models import Notification


def notifications_context(request):
    """Context processor pour les notifications non lues des super_users"""
    context = {}
    
    if request.user.is_authenticated and request.user.is_superuser:
        notifications_non_lues = Notification.objects.filter(lu=False).count()
        context['notifications_non_lues_count'] = notifications_non_lues
    else:
        context['notifications_non_lues_count'] = 0
    
    return context
