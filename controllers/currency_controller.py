from PyQt6.QtCore import QObject, pyqtSignal
import json
from datetime import datetime


class CurrencyController(QObject):
    """
    Contrôleur pour la conversion de devises.
    Gère la récupération et l'utilisation des taux de change.
    """

    # Signaux
    rates_updated = pyqtSignal()
    conversion_result = pyqtSignal(float, str)  # montant, devise
    error_occurred = pyqtSignal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.rates = {}
        self.last_update = None
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur."""
        self.view.convert_clicked.connect(self.convert_currency)
        self.view.update_rates_clicked.connect(self.update_rates)

    def get_available_currencies(self):
        """Retourne la liste des devises disponibles."""
        return list(self.rates.keys())

    def update_rates(self):
        """Met à jour les taux de change."""
        try:
            self.view.set_loading(True)
            self.model.update_rates()
            self.rates = self.model.get_rates()
            self.last_update = self.model.get_last_update()
            self.view.set_last_update(self.last_update)
            self.rates_updated.emit()

            # Mettre à jour les devises dans la vue
            self.view.set_currencies(self.get_available_currencies())

        except Exception as e:
            self.error_occurred.emit(
                f"Erreur lors de la mise à jour des taux: {str(e)}"
            )
        finally:
            self.view.set_loading(False)

    def convert_currency(self, amount, from_currency, to_currency):
        """
        Convertit un montant d'une devise à une autre.

        Args:
            amount: Montant à convertir
            from_currency: Devise source
            to_currency: Devise cible
        """
        try:
            if not all([amount, from_currency, to_currency]):
                self.error_occurred.emit("Tous les champs sont obligatoires")
                return

            amount = float(amount)

            if from_currency == to_currency:
                self.conversion_result.emit(amount, to_currency)
                return

            if not self.rates:
                self.error_occurred.emit("Les taux de change ne sont pas disponibles")
                return

            if from_currency not in self.rates or to_currency not in self.rates:
                self.error_occurred.emit(
                    "Une ou plusieurs devises ne sont pas prises en charge"
                )
                return

            # Conversion via EUR (taux croisés)
            if from_currency == "EUR":
                result = amount * self.rates[to_currency]
            elif to_currency == "EUR":
                result = amount / self.rates[from_currency]
            else:
                # Conversion via EUR (taux croisés)
                eur_amount = amount / self.rates[from_currency]
                result = eur_amount * self.rates[to_currency]

            # Calcul du taux de change actuel
            rate = result / amount if amount != 0 else 0
            self.view.set_exchange_rate(rate, from_currency, to_currency)

            self.conversion_result.emit(round(result, 4), to_currency)

        except ValueError:
            self.error_occurred.emit("Veuillez entrer un montant valide")
        except Exception as e:
            self.error_occurred.emit(f"Erreur de conversion: {str(e)}")

    def load_rates_from_cache(self):
        """Charge les taux depuis le cache."""
        try:
            self.rates = self.model.load_rates()
            self.last_update = self.model.get_last_update()
            self.view.set_last_update(self.last_update)

            # Mettre à jour les devises dans la vue
            if self.rates:
                self.view.set_currencies(self.get_available_currencies())

        except Exception as e:
            self.error_occurred.emit(f"Erreur lors du chargement du cache: {str(e)}")

    def initialize(self):
        """Initialise le contrôleur."""
        self.load_rates_from_cache()

        # Si pas de données en cache, on met à jour les taux
        if not self.rates:
            self.update_rates()
