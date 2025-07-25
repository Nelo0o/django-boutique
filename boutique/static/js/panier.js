class PanierManager {
    constructor() {
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        this.init();
    }

    init() {
        // Event listeners
        document.addEventListener('click', (e) => this.handleClick(e));
        
        // Mettre à jour le compteur au chargement
        this.updateCartCount();
    }

    handleClick(e) {
        // Ajouter au panier
        if (e.target.closest('.add-to-cart-btn')) {
            e.preventDefault();
            this.ajouterAuPanier(e.target.closest('.add-to-cart-btn'));
        }
        
        // Supprimer du panier
        if (e.target.closest('.remove-from-cart-btn')) {
            e.preventDefault();
            this.supprimerDuPanier(e.target.closest('.remove-from-cart-btn'));
        }
        
        // Vider le panier
        if (e.target.closest('.clear-cart-btn')) {
            e.preventDefault();
            console.log('Bouton vider panier cliqué');
            this.viderPanier();
        }
    }

    async ajouterAuPanier(btn) {
        if (btn.disabled) return;
        
        const produitId = btn.dataset.produitId;
        if (!produitId) return;
        
        btn.disabled = true;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>AJOUT...';
        
        try {
            const response = await fetch(`/panier/ajouter/${produitId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(data.message, 'success');
                this.updateCartCount(data.nombre_articles);
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.showToast('Une erreur est survenue', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    }

    async supprimerDuPanier(btn) {
        const produitId = btn.dataset.produitId;
        if (!produitId) return;
        
        try {
            const response = await fetch(`/panier/supprimer/${produitId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(data.message, 'success');
                this.updateCartCount(data.nombre_articles);
                
                // Supprimer l'élément du DOM
                const cartItem = btn.closest('.cart-item');
                if (cartItem) {
                    cartItem.remove();
                }
                
                // Recharger si panier vide
                if (data.nombre_articles === 0) {
                    setTimeout(() => location.reload(), 1000);
                }
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.showToast('Une erreur est survenue', 'error');
        }
    }

    async viderPanier() {
        try {
            const response = await fetch('/panier/vider/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(data.message, 'success');
                this.updateCartCount(0);
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.showToast('Une erreur est survenue', 'error');
        }
    }

    updateCartCount(count = null) {
        const cartCountElements = document.querySelectorAll('.cart-count');
        
        if (count !== null) {
            // Mettre à jour avec la valeur fournie
            cartCountElements.forEach(el => {
                el.textContent = count;
                // Cacher si 0
                el.style.display = count > 0 ? 'flex' : 'none';
            });
        } else {
            // Récupérer le nombre depuis la session
            fetch('/panier/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                // Extraire le nombre d'articles depuis la réponse
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const countElement = doc.querySelector('[data-cart-count]');
                const count = countElement ? parseInt(countElement.dataset.cartCount) : 0;
                
                cartCountElements.forEach(el => {
                    el.textContent = count;
                    el.style.display = count > 0 ? 'flex' : 'none';
                });
            })
            .catch(error => console.error('Erreur lors de la récupération du compteur:', error));
        }
    }

    showToast(message, type = 'success') {
        // Créer le conteneur s'il n'existe pas
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'fixed top-4 right-4 z-50 space-y-2';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast px-6 py-4 rounded-lg shadow-lg text-white font-semibold transform translate-x-full opacity-0 transition-all duration-300 ${
            type === 'success' ? 'bg-green-600' : 'bg-red-600'
        }`;
        
        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        toast.innerHTML = `
            <div class="flex items-center space-x-3">
                <i class="fas ${icon}"></i>
                <span>${message}</span>
            </div>
        `;
        
        container.appendChild(toast);
        
        // Animation d'entrée
        setTimeout(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
        }, 100);
        
        // Suppression automatique
        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Initialiser quand le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    window.panierManager = new PanierManager();
});
