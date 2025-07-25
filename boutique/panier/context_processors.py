def panier_count(request):
    """Context processor pour le nombre d'articles dans le panier"""
    panier = request.session.get('panier', {})
    return {
        'panier_count': sum(panier.values())
    }
