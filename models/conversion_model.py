from typing import Dict, List
from datetime import datetime


class ConversionModel:
    """
    Modèle pour les conversions d'unités.
    Gère les conversions entre différentes unités de mesure.
    """

    # Facteurs de conversion (exemple simplifié)
    CONVERSION_FACTORS = {
        "Longueur": {
            "m": 1.0,
            "km": 1000.0,
            "cm": 0.01,
            "mm": 0.001,
            "in": 0.0254,
            "ft": 0.3048,
            "yd": 0.9144,
            "mi": 1609.34,
        },
        "Masse": {
            "kg": 1.0,
            "g": 0.001,
            "mg": 0.000001,
            "lb": 0.453592,
            "oz": 0.0283495,
        },
        "Température": {"C": "celsius", "F": "fahrenheit", "K": "kelvin"},
        "Volume": {
            "L": 1.0,
            "mL": 0.001,
            "m³": 1000.0,
            "ft³": 28.3168,
            "gal": 3.78541,
            "pt": 0.473176,
        },
        "Temps": {"s": 1.0, "ms": 0.001, "min": 60.0, "h": 3600.0, "d": 86400.0},
    }

    def __init__(self):
        self.history = []

    def get_categories(self) -> List[str]:
        """
        Retourne la liste des catégories de conversion disponibles.

        Returns:
            Liste des catégories
        """
        return list(self.CONVERSION_FACTORS.keys())

    def get_units_for_category(self, category: str) -> List[str]:
        """
        Retourne la liste des unités disponibles pour une catégorie.

        Args:
            category: La catégorie d'unités

        Returns:
            Liste des unités
        """
        return list(self.CONVERSION_FACTORS.get(category, {}).keys())

    def convert(
        self, value: float, from_unit: str, to_unit: str, conv_type: str
    ) -> float:
        """
        Convertit une valeur d'une unité à une autre.

        Args:
            value: La valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
            conv_type: Type de conversion

        Returns:
            La valeur convertie
        """
        try:
            # Vérifie si les unités sont valides pour cette catégorie
            if from_unit not in self.CONVERSION_FACTORS.get(
                conv_type, {}
            ) or to_unit not in self.CONVERSION_FACTORS.get(conv_type, {}):
                raise ValueError("Unités non prises en charge pour cette catégorie")

            # Gestion spéciale pour la température
            if conv_type == "Température":
                return self._convert_temperature(value, from_unit, to_unit)

            # Conversion standard pour les autres unités
            factor_from = self.CONVERSION_FACTORS[conv_type][from_unit]
            factor_to = self.CONVERSION_FACTORS[conv_type][to_unit]

            # Conversion via l'unité de base (m, kg, L, etc.)
            base_value = value * factor_from
            result = base_value / factor_to

            # Ajoute à l'historique
            self.history.append(
                {
                    "value": value,
                    "from_unit": from_unit,
                    "to_unit": to_unit,
                    "result": result,
                    "type": conv_type,
                    "timestamp": self._get_timestamp(),
                }
            )

            return result

        except Exception as e:
            raise ValueError(f"Erreur de conversion: {str(e)}")

    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convertit une température entre différentes unités.

        Args:
            value: La température à convertir
            from_unit: Unité source (C, F, K)
            to_unit: Unité cible (C, F, K)

        Returns:
            La température convertie
        """
        # Conversion vers Celsius en premier
        if from_unit == "C":
            celsius = value
        elif from_unit == "F":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "K":
            celsius = value - 273.15
        else:
            raise ValueError("Unité de température source non reconnue")

        # Conversion de Celsius vers l'unité cible
        if to_unit == "C":
            return celsius
        elif to_unit == "F":
            return (celsius * 9 / 5) + 32
        elif to_unit == "K":
            return celsius + 273.15
        else:
            raise ValueError("Unité de température cible non reconnue")

    def get_conversion_history(self) -> List[Dict]:
        """
        Retourne l'historique des conversions.

        Returns:
            Liste des conversions effectuées
        """
        return self.history

    def clear_history(self):
        """Efface l'historique des conversions."""
        self.history = []

    def _get_timestamp(self) -> str:
        """
        Retourne un horodatage au format lisible.

        Returns:
            Chaîne de caractères représentant la date et l'heure actuelles
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
