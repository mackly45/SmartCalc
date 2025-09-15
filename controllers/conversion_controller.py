from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, List, Optional


class ConversionController(QObject):
    """
    Contrôleur pour les conversions d'unités.
    Gère la logique de conversion entre différentes unités de mesure.
    """

    # Signaux
    conversion_result = pyqtSignal(str)  # Résultat de la conversion
    error_occurred = pyqtSignal(str)  # Message d'erreur

    # Catégories de conversion disponibles
    CONVERSION_CATEGORIES = {
        "Longueur": ["mètres", "kilomètres", "milles", "pieds", "pouces"],
        "Masse": ["grammes", "kilogrammes", "livres", "onces"],
        "Température": ["Celsius", "Fahrenheit", "Kelvin"],
        "Volume": ["litres", "millilitres", "gallons", "pintes"],
        "Surface": ["m²", "pieds²", "hectares", "acres"],
    }

    # Facteurs de conversion
    CONVERSION_FACTORS = {
        # Longueur (en mètres)
        "mètres": 1.0,
        "kilomètres": 1000.0,
        "milles": 1609.34,
        "pieds": 0.3048,
        "pouces": 0.0254,
        # Masse (en grammes)
        "grammes": 1.0,
        "kilogrammes": 1000.0,
        "livres": 453.592,
        "onces": 28.3495,
        # Volume (en litres)
        "litres": 1.0,
        "millilitres": 0.001,
        "gallons": 3.78541,
        "pintes": 0.568261,
        # Surface (en mètres carrés)
        "m²": 1.0,
        "pieds²": 0.092903,
        "hectares": 10000.0,
        "acres": 4046.86,
    }

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        self.view.convert_clicked.connect(self.convert_units)
        self.view.category_changed.connect(self.update_units)

    def get_categories(self) -> List[str]:
        """Retourne la liste des catégories de conversion"""
        return list(self.CONVERSION_CATEGORIES.keys())

    def get_units_for_category(self, category: str) -> List[str]:
        """
        Retourne les unités disponibles pour une catégorie donnée.

        Args:
            category: La catégorie d'unités

        Returns:
            Liste des unités disponibles
        """
        return self.CONVERSION_CATEGORIES.get(category, [])

    def update_units(self, category: str) -> None:
        """
        Met à jour les unités disponibles dans la vue.

        Args:
            category: La catégorie sélectionnée
        """
        units = self.get_units_for_category(category)
        self.view.update_unit_comboboxes(units)

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> None:
        """
        Convertit une valeur d'une unité à une autre.

        Args:
            value: La valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
        """
        try:
            if self._is_temperature_conversion(from_unit, to_unit):
                result = self._convert_temperature(value, from_unit, to_unit)
            else:
                result = self._convert_standard(value, from_unit, to_unit)

            self.conversion_result.emit(f"{value} {from_unit} = {result:.6f} {to_unit}")

        except (ValueError, KeyError) as e:
            self.error_occurred.emit(f"Erreur de conversion: {str(e)}")

    def _is_temperature_conversion(self, from_unit: str, to_unit: str) -> bool:
        """Vérifie s'il s'agit d'une conversion de température"""
        temp_units = self.CONVERSION_CATEGORIES["Température"]
        return from_unit in temp_units or to_unit in temp_units

    def _convert_standard(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Effectue une conversion standard basée sur des facteurs.

        Args:
            value: Valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible

        Returns:
            La valeur convertie
        """
        try:
            base_value = value * self.CONVERSION_FACTORS[from_unit]
            return base_value / self.CONVERSION_FACTORS[to_unit]
        except KeyError as e:
            raise ValueError(f"Unité non supportée: {e}")

    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convertit une température entre différentes unités.

        Args:
            value: Température à convertir
            from_unit: Unité source (C, F, K)
            to_unit: Unité cible (C, F, K)

        Returns:
            La température convertie
        """
        # D'abord convertir en Celsius
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            raise ValueError(f"Unité non supportée: {from_unit}")

        # Puis convertir de Celsius vers l'unité cible
        if to_unit == "Celsius":
            return celsius
        elif to_unit == "Fahrenheit":
            return (celsius * 9 / 5) + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15
        else:
            raise ValueError(f"Unité non supportée: {to_unit}")
