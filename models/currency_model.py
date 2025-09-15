import json
import os
from datetime import datetime, timedelta
import requests
from PyQt6.QtCore import QObject, pyqtSignal


class CurrencyModel(QObject):
    rates_updated = pyqtSignal(bool, str)  # success, message

    def __init__(self):
        super().__init__()
        self.rates = {}
        self.last_updated = None
        self.base_currency = "USD"
        self.cache_file = "currency_rates.json"
        self.load_rates_from_cache()

    def get_available_currencies(self):
        """Retourne la liste des devises disponibles"""
        return [
            ("USD", "Dollar américain ($)"),
            ("EUR", "Euro (€)"),
            ("XOF", "Franc CFA Ouest-africain (CFA)"),
            ("XAF", "Franc CFA Centrafricain (FCFA)"),
            ("CDF", "Franc congolais (FC)"),
            ("XPF", "Franc CFP (XPF)"),
            ("MAD", "Dirham marocain (MAD)"),
            ("TND", "Dinar tunisien (DT)"),
            ("DZD", "Dinar algérien (DA)"),
            ("EGP", "Livre égyptienne (LE)"),
            ("NGN", "Naira nigérian (₦)"),
            ("ZAR", "Rand sud-africain (R)"),
            ("GBP", "Livre sterling (£)"),
            ("JPY", "Yen japonais (¥)"),
            ("CNY", "Yuan chinois (¥)"),
            ("RUB", "Rouble russe (₽)"),
        ]

    def load_rates_from_cache(self):
        """Charge les taux depuis le cache local"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    data = json.load(f)
                    self.rates = data.get("rates", {})
                    last_updated = data.get("last_updated")
                    self.last_updated = (
                        datetime.fromisoformat(last_updated) if last_updated else None
                    )
                    self.base_currency = data.get("base", "USD")
                    return True
            except Exception as e:
                print(f"Erreur lors du chargement du cache: {e}")
        return False

    def save_rates_to_cache(self):
        """Sauvegarde les taux dans le cache local"""
        try:
            data = {
                "rates": self.rates,
                "last_updated": datetime.now().isoformat(),
                "base": self.base_currency,
            }
            with open(self.cache_file, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du cache: {e}")
            return False

    def update_rates(self, api_key=None):
        """Met à jour les taux de change depuis l'API"""
        if not api_key:
            # Mode hors ligne - utiliser les taux en cache s'ils existent
            if self.rates:
                self.rates_updated.emit(True, "Taux chargés depuis le cache")
                return True
            self.rates_updated.emit(
                False, "Clé API manquante et aucun cache disponible"
            )
            return False

        try:
            # Essayer d'abord avec l'API principale
            response = requests.get(
                f"https://api.exchangerate.host/latest?base={self.base_currency}",
                timeout=10,  # Timeout après 10 secondes
            )
            data = response.json()

            if data.get("success", False):
                self.rates = data.get("rates", {})
                # S'assurer que la devise de base a un taux de 1.0
                if self.base_currency not in self.rates:
                    self.rates[self.base_currency] = 1.0
                self.last_updated = datetime.now()
                self.save_rates_to_cache()
                self.rates_updated.emit(True, "Taux de change mis à jour avec succès")
                return True
            else:
                error = data.get("error", {})
                error_msg = f"Erreur API: {error.get('info', 'Erreur inconnue')}"
                print(error_msg)
                self.rates_updated.emit(False, error_msg)
                return False

        except requests.exceptions.RequestException as e:
            error_msg = f"Erreur de connexion: {str(e)}"
            print(error_msg)
            self.rates_updated.emit(False, error_msg)
            return False
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            print(error_msg)
            self.rates_updated.emit(False, error_msg)
            return False

    def convert(self, amount, from_currency, to_currency):
        """Convertit un montant d'une devise à une autre"""
        if from_currency == to_currency:
            return amount

        if not self.rates:
            self.rates_updated.emit(False, "Aucun taux de change disponible")
            return None

        try:
            # Si la devise source est la devise de base
            if from_currency == self.base_currency:
                rate = self.rates.get(to_currency)
                if rate is None:
                    return None
                return amount * rate

            # Si la devise cible est la devise de base
            if to_currency == self.base_currency:
                rate = self.rates.get(from_currency)
                if rate is None or rate == 0:
                    return None
                return amount / rate

            # Conversion via la devise de base
            from_rate = self.rates.get(from_currency)
            to_rate = self.rates.get(to_currency)

            if from_rate is None or to_rate is None or from_rate == 0:
                return None

            return amount * (to_rate / from_rate)

        except Exception as e:
            print(f"Erreur lors de la conversion: {e}")
            return None

    def get_rate(self, from_currency, to_currency):
        """Obtient le taux de change entre deux devises"""
        if from_currency == to_currency:
            return 1.0

        if not self.rates:
            return None

        try:
            if from_currency == self.base_currency:
                return self.rates.get(to_currency)

            if to_currency == self.base_currency:
                rate = self.rates.get(from_currency)
                return 1.0 / rate if rate else None

            from_rate = self.rates.get(from_currency)
            to_rate = self.rates.get(to_currency)

            if from_rate is None or to_rate is None or from_rate == 0:
                return None

            return to_rate / from_rate

        except Exception as e:
            print(f"Erreur lors du calcul du taux: {e}")
            return None
