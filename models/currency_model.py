import json
import os
from datetime import datetime, timedelta
import requests
from typing import Dict, Optional


class CurrencyModel:
    """
    Modèle pour la conversion de devises.
    Gère la récupération et le stockage des taux de change.
    """

    # URL de l'API de taux de change (exemple avec exchangerate-api.com)
    API_URL = "https://v6.exchangerate-api.com/v6/{}/latest/EUR"

    # Fichier de cache pour les taux
    CACHE_FILE = "currency_rates.json"

    # Durée de validité du cache (en heures)
    CACHE_EXPIRY_HOURS = 24

    def __init__(self, api_key: str = None):
        """
        Initialise le modèle de devise.

        Args:
            api_key: Clé API pour le service de taux de change
        """
        self.api_key = api_key or os.getenv("EXCHANGE_RATE_API_KEY")
        self.rates = {}
        self.last_update = None
        self.base_currency = "EUR"

    def get_rates(self) -> Dict[str, float]:
        """
        Récupère les taux de change actuels.

        Returns:
            Dictionnaire des taux de change par rapport à la devise de base
        """
        # Vérifie d'abord le cache
        if self._is_cache_valid():
            return self.rates

        # Si le cache n'est pas valide, met à jour les taux
        self.update_rates()
        return self.rates

    def update_rates(self) -> bool:
        """
        Met à jour les taux de change depuis l'API.

        Returns:
            True si la mise à jour a réussi, False sinon
        """
        if not self.api_key:
            raise ValueError("Clé API manquante pour le service de taux de change")

        try:
            # Appel à l'API
            url = self.API_URL.format(self.api_key)
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("result") != "success":
                raise ValueError("Échec de la récupération des taux de change")

            # Met à jour les taux et la date de dernière mise à jour
            self.rates = data.get("conversion_rates", {})
            self.base_currency = data.get("base_code", "EUR")
            self.last_update = datetime.now()

            # Met en cache les données
            self._save_to_cache()

            return True

        except requests.RequestException as e:
            # En cas d'erreur, essaie de charger les données du cache
            if self._load_from_cache():
                return True
            raise ConnectionError(
                f"Impossible de mettre à jour les taux de change: {str(e)}"
            )

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convertit un montant d'une devise à une autre.

        Args:
            amount: Montant à convertir
            from_currency: Code de la devise source (ex: 'EUR')
            to_currency: Code de la devise cible (ex: 'USD')

        Returns:
            Le montant converti
        """
        if not self.rates:
            self.get_rates()

        # Vérifie que les devises sont valides
        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError("Une ou plusieurs devises ne sont pas prises en charge")

        # Si les devises sont identiques, retourne le montant inchangé
        if from_currency == to_currency:
            return amount

        # Conversion via la devise de base (EUR)
        if from_currency == self.base_currency:
            return amount * self.rates[to_currency]
        elif to_currency == self.base_currency:
            return amount / self.rates[from_currency]
        else:
            # Conversion via la devise de base (EUR)
            eur_amount = amount / self.rates[from_currency]
            return eur_amount * self.rates[to_currency]

    def get_last_update(self) -> Optional[datetime]:
        """
        Retourne la date de dernière mise à jour des taux.

        Returns:
            Objet datetime ou None si jamais mis à jour
        """
        return self.last_update

    def _is_cache_valid(self) -> bool:
        """
        Vérifie si le cache est toujours valide.

        Returns:
            True si le cache est valide, False sinon
        """
        if not self.last_update or not os.path.exists(self.CACHE_FILE):
            return False

        cache_age = datetime.now() - self.last_update
        return cache_age < timedelta(hours=self.CACHE_EXPIRY_HOURS)

    def _save_to_cache(self) -> bool:
        """
        Sauvegarde les taux actuels dans le cache.

        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        try:
            data = {
                "rates": self.rates,
                "base_currency": self.base_currency,
                "last_update": (
                    self.last_update.isoformat() if self.last_update else None
                ),
            }

            with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return True

        except (IOError, json.JSONEncodeError):
            return False

    def _load_from_cache(self) -> bool:
        """
        Charge les taux depuis le cache.

        Returns:
            True si le chargement a réussi, False sinon
        """
        try:
            if not os.path.exists(self.CACHE_FILE):
                return False

            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.rates = data.get("rates", {})
            self.base_currency = data.get("base_currency", "EUR")

            last_update_str = data.get("last_update")
            if last_update_str:
                self.last_update = datetime.fromisoformat(last_update_str)

            return True

        except (IOError, json.JSONDecodeError, ValueError):
            return False

    def get_supported_currencies(self) -> list:
        """
        Retourne la liste des devises prises en charge.

        Returns:
            Liste des codes de devises
        """
        if not self.rates:
            self.get_rates()
        return list(self.rates.keys())
