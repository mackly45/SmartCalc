from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import requests
from datetime import datetime


class CurrencyController(QObject):
    """
    Contrôleur pour le convertisseur de devises.
    Gère la logique de conversion et la communication entre le modèle et la vue.
    """

    def __init__(self, model, view):
        """
        Initialise le contrôleur avec le modèle et la vue.

        Args:
            model: Instance de CurrencyModel
            view: Instance de CurrencyView
        """
        super().__init__()
        self.model = model
        self.view = view

        # Configuration initiale
        self.setup_connections()
        self.initialize_ui()

    def setup_connections(self):
        """Établit les connexions entre les signaux et les slots"""
        # Connexion des signaux de la vue
        self.view.convert_requested.connect(self.convert_currency)
        self.view.update_rates_requested.connect(self.update_rates)

        # Connexion des signaux du modèle
        self.model.rates_updated.connect(self.on_rates_updated)

    def initialize_ui(self):
        """Initialise l'interface utilisateur avec les données du modèle"""
        # Charger la liste des devises disponibles
        currencies = self.model.get_available_currencies()
        self.view.set_currencies(currencies)

        # Vérifier si des taux sont déjà chargés
        if hasattr(self.model, "rates") and self.model.rates:
            self.view.set_status("Taux chargés depuis le cache")
        else:
            self.view.set_status(
                "Appuyez sur 'Mettre à jour les taux' pour charger les taux de change"
            )

    def convert_currency(self, amount, from_currency, to_currency):
        """
        Convertit un montant d'une devise à une autre.

        Args:
            amount: Montant à convertir
            from_currency: Code de la devise source (ex: 'EUR')
            to_currency: Code de la devise cible (ex: 'USD')
        """
        if not from_currency or not to_currency:
            self.view.set_status(
                "Veuillez sélectionner des devises valides", is_error=True
            )
            return

        try:
            # Vérifier si les devises sont identiques
            if from_currency == to_currency:
                self.view.set_conversion_result(amount, 1.0)
                return

            # Obtenir le taux de change
            rate = self.model.get_rate(from_currency, to_currency)

            if rate is None:
                # Essayer de forcer une mise à jour des taux
                self.view.set_status("Taux non disponible, mise à jour en cours...")
                self.update_rates()
                # Réessayer après un court délai
                QTimer.singleShot(
                    1000,
                    lambda: self.retry_conversion(amount, from_currency, to_currency),
                )
                return

            # Effectuer la conversion
            result = amount * rate

            # Mettre à jour l'interface
            self.view.set_conversion_result(result, rate)

        except Exception as e:
            self.view.set_status(
                f"Erreur lors de la conversion: {str(e)}", is_error=True
            )

    def retry_conversion(self, amount, from_currency, to_currency):
        """
        Réessaie une conversion après une mise à jour des taux.

        Args:
            amount: Montant à convertir
            from_currency: Code de la devise source
            to_currency: Code de la devise cible
        """
        rate = self.model.get_rate(from_currency, to_currency)
        if rate is not None:
            result = amount * rate
            self.view.set_conversion_result(result, rate)
            self.view.set_status(
                "Conversion effectuée avec les derniers taux disponibles"
            )
        else:
            self.view.set_status(
                "Impossible d'obtenir le taux de change. Vérifiez votre connexion.",
                is_error=True,
            )

    def update_rates(self):
        """Met à jour les taux de change depuis l'API"""
        self.view.set_loading(True)
        self.view.set_status("Mise à jour des taux en cours...")

        # Utiliser une clé API vide pour utiliser le mode gratuit de l'API
        try:
            # Essayer d'abord avec l'API gratuite
            success = self.model.update_rates(api_key="")

            if not success:
                # Si l'API gratuite échoue, essayer avec une autre source
                success = self.try_alternative_api()

            if not success and not self.model.rates:
                self.view.set_status(
                    "Impossible de mettre à jour les taux. Mode hors ligne activé.",
                    is_error=True,
                )

        except Exception as e:
            print(f"Erreur lors de la mise à jour des taux: {e}")
            self.view.set_status(
                "Erreur lors de la mise à jour des taux", is_error=True
            )

        self.view.set_loading(False)

    def try_alternative_api(self):
        """Essaie une autre source pour les taux de change"""
        try:
            # Essayer avec une autre API gratuite
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            if response.status_code == 200:
                data = response.json()
                self.model.rates = data.get("rates", {})
                self.model.last_updated = datetime.now()
                self.model.base_currency = data.get("base", "USD")
                self.model.save_rates_to_cache()
                self.model.rates_updated.emit(
                    True, "Taux mis à jour avec succès (source alternative)"
                )
                return True
        except Exception as e:
            print(f"Erreur avec l'API alternative: {e}")

        return False

    def on_rates_updated(self, success, message):
        """
        Gère la mise à jour des taux de change.

        Args:
            success: True si la mise à jour a réussi, False sinon
            message: Message détaillant le résultat de l'opération
        """
        if success:
            self.view.set_status(message)
            # Si une conversion était en attente, on la relance
            amount, from_curr, to_curr = self.view.get_conversion_data()
            if amount > 0 and from_curr and to_curr:
                self.convert_currency(amount, from_curr, to_curr)
        else:
            self.view.set_status(message, is_error=True)

    def cleanup(self):
        """Nettoie les ressources utilisées par le contrôleur"""
        # Sauvegarder les taux dans le cache avant de quitter
        self.model.save_rates_to_cache()
