from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Union

class ConversionType(Enum):
    """Énumération des types de conversion disponibles"""
    LENGTH = "Longueur"
    MASS = "Masse"
    TEMPERATURE = "Température"
    TIME = "Temps"
    VOLUME = "Volume"
    AREA = "Surface"
    SPEED = "Vitesse"
    DATA = "Données"

class ConversionModel:
    """Modèle pour gérer les conversions d'unités"""
    
    def __init__(self):
        # Facteurs de conversion pour chaque type d'unité
        # Les valeurs sont exprimées en unités de base (m, kg, s, etc.)
        self.conversion_factors = {
            # Longueur (mètre comme unité de base)
            ConversionType.LENGTH: {
                'm': 1.0,
                'km': 1000.0,
                'cm': 0.01,
                'mm': 0.001,
                'μm': 1e-6,
                'nm': 1e-9,
                'in': 0.0254,
                'ft': 0.3048,
                'yd': 0.9144,
                'mi': 1609.34,
                'nmi': 1852.0
            },
            # Masse (kilogramme comme unité de base)
            ConversionType.MASS: {
                'kg': 1.0,
                'g': 0.001,
                'mg': 0.000001,
                'μg': 1e-9,
                't': 1000.0,
                'lb': 0.453592,
                'oz': 0.0283495,
                'st': 6.35029,
                'ct': 0.0002
            },
            # Température (gestion spéciale)
            ConversionType.TEMPERATURE: {
                '°C': 'celsius',
                '°F': 'fahrenheit',
                'K': 'kelvin',
                '°R': 'rankine'
            },
            # Temps (seconde comme unité de base)
            ConversionType.TIME: {
                's': 1.0,
                'ms': 0.001,
                'μs': 1e-6,
                'ns': 1e-9,
                'min': 60.0,
                'h': 3600.0,
                'j': 86400.0,
                'sem': 604800.0,
                'an': 31536000.0  # année non bissextile
            },
            # Volume (litre comme unité de base)
            ConversionType.VOLUME: {
                'L': 1.0,
                'mL': 0.001,
                'm³': 1000.0,
                'cm³': 0.001,
                'ft³': 28.3168,
                'in³': 0.0163871,
                'gal (US)': 3.78541,
                'gal (UK)': 4.54609,
                'pt (US)': 0.473176,
                'pt (UK)': 0.568261
            },
            # Surface (mètre carré comme unité de base)
            ConversionType.AREA: {
                'm²': 1.0,
                'km²': 1000000.0,
                'cm²': 0.0001,
                'mm²': 1e-6,
                'ha': 10000.0,
                'ac': 4046.86,
                'ft²': 0.092903,
                'in²': 0.00064516,
                'mi²': 2589988.11
            },
            # Vitesse (mètre par seconde comme unité de base)
            ConversionType.SPEED: {
                'm/s': 1.0,
                'km/h': 0.277778,
                'mph': 0.44704,
                'nœud': 0.514444,
                'ft/s': 0.3048
            },
            # Données (octet comme unité de base)
            ConversionType.DATA: {
                'o': 1.0,
                'Ko': 1024.0,
                'Mo': 1048576.0,
                'Go': 1073741824.0,
                'To': 1099511627776.0,
                'Kio': 1000.0,
                'Mio': 1000000.0,
                'Gio': 1000000000.0,
                'Tio': 1000000000000.0
            }
        }

    def get_conversion_types(self) -> List[str]:
        """Retourne la liste des types de conversion disponibles"""
        return [t.value for t in ConversionType]

    def get_units(self, conversion_type: str) -> List[str]:
        """
        Retourne la liste des unités disponibles pour un type de conversion donné
        
        Args:
            conversion_type: Le type de conversion (valeur de ConversionType)
            
        Returns:
            Liste des unités disponibles pour ce type de conversion
        """
        conv_type = next((t for t in ConversionType if t.value == conversion_type), None)
        if conv_type and conv_type in self.conversion_factors:
            return list(self.conversion_factors[conv_type].keys())
        return []

    def convert(self, value: float, from_unit: str, to_unit: str, conversion_type: str) -> Optional[float]:
        """
        Effectue une conversion d'unité
        
        Args:
            value: La valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
            conversion_type: Type de conversion
            
        Returns:
            La valeur convertie ou None en cas d'erreur
        """
        try:
            # Vérifier les entrées
            if not isinstance(value, (int, float)):
                return None
                
            # Trouver le type de conversion
            conv_type = next((t for t in ConversionType if t.value == conversion_type), None)
            if not conv_type or conv_type not in self.conversion_factors:
                return None

            units = self.conversion_factors[conv_type]
            if from_unit not in units or to_unit not in units:
                return None

            # Gestion spéciale pour la température
            if conv_type == ConversionType.TEMPERATURE:
                return self._convert_temperature(value, from_unit, to_unit)

            # Conversion standard pour les autres types
            value_in_base = value * units[from_unit]
            return value_in_base / units[to_unit]

        except (ValueError, KeyError, TypeError):
            return None

    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convertit entre différentes échelles de température
        
        Args:
            value: Valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
            
        Returns:
            Température convertie
        """
        if from_unit == to_unit:
            return value

        # Convertir d'abord en Celsius (unité intermédiaire)
        if from_unit == '°C':
            celsius = value
        elif from_unit == '°F':
            celsius = (value - 32) * 5/9
        elif from_unit == 'K':
            celsius = value - 273.15
        elif from_unit == '°R':
            celsius = (value - 491.67) * 5/9
        else:
            return value  # Unité inconnue

        # Puis convertir de Celsius vers l'unité cible
        if to_unit == '°C':
            return celsius
        elif to_unit == '°F':
            return (celsius * 9/5) + 32
        elif to_unit == 'K':
            return celsius + 273.15
        elif to_unit == '°R':
            return (celsius + 273.15) * 9/5
        
        return value  # Unité cible inconnue

    def get_conversion_history(self) -> List[Dict]:
        """
        Retourne l'historique des conversions
        
        Note: À implémenter avec une base de données pour la persistance
        """
        return []
