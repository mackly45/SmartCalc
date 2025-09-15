from PyQt6.QtCore import QObject
from typing import Dict, Optional, List
import requests
import json
from datetime import datetime, timedelta


class CurrencyController(QObject):
    """
    Contrôleur pour les opérations de conversion de devises.
    Gère la récupération des taux de change et les conversions.
    """

    # Signaux
    conversion_result = QObject().pyqtSignal(str)
    error_occurred = QObject().pyqtSignal(str)
    rates_updated = QObject().pyqtSignal()

    # URL de l'API de taux de change
    API_URL = "https://api.exchangerate-api.com/v4/latest/EUR"

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.rates = {}
        self.last_update = None
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        self.view.convert_clicked.connect(self.convert_currency)
        self.view.update_rates_clicked.connect(self.update_exchange_rates)

    def get_available_currencies(self) -> List[str]:
        """Retourne la liste des devises disponibles"""
        if not self.rates:
            self.load_rates_from_cache()
        return list(self.rates.keys())

    def load_rates_from_cache(self) -> None:
        """Charge les taux depuis le cache local"""
        try:
            with open("currency_rates.json", "r") as f:
                data = json.load(f)
                self.rates = data.get("rates", {})
                self.last_update = datetime.fromisoformat(data.get("last_update", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            self.rates = {"EUR": 1.0}  # Taux par défaut

    def save_rates_to_cache(self) -> None:
        """Sauvegarde les taux en cache local"""
        with open("currency_rates.json", "w") as f:
            data = {"rates": self.rates, "last_update": self.last_update.isoformat()}
            json.dump(data, f)

    def update_exchange_rates(self) -> None:
        """Met à jour les taux de change depuis l'API"""
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()
            data = response.json()

            self.rates = data.get("rates", {})
            self.last_update = datetime.now()
            self.save_rates_to_cache()
            self.rates_updated.emit()

        except requests.RequestException as e:
            self.error_occurred.emit(
                f"Erreur lors de la mise à jour des taux: {str(e)}"
            )

    def convert_currency(
        self, amount: float, from_currency: str, to_currency: str
    ) -> None:
        """
        Convertit un montant d'une devise à une autre.

        Args:
            amount: Montant à convertir
            from_currency: Devise source
            to_currency: Devise cible
        """
        try:
            if not self.rates:
                self.load_rates_from_cache()

            if from_currency not in self.rates or to_currency not in self.rates:
                self.error_occurred.emit(
                    "Une ou plusieurs devises ne sont pas disponibles"
                )
                return

            # Conversion via EUR (taux croisés)
            eur_amount = amount / self.rates[from_currency]
            result = eur_amount * self.rates[to_currency]

            self.conversion_result.emit(
                f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}"
            )

        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de la conversion: {str(e)}")

    def get_last_update_time(self) -> Optional[str]:
        """Retourne la date de dernière mise à jour des taux"""
        if self.last_update:
            return self.last_update.strftime("%d/%m/%Y %H:%M")
        return None
