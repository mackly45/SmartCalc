"""
Package contenant les modèles de données de l'application SmartCalc.

Ce package inclut les modèles suivants :
- calculator_model : Modèle pour la calculatrice de base
- scientific_model : Modèle pour les fonctions scientifiques
- currency_model : Modèle pour la conversion de devises
- conversion_model : Modèle pour la conversion d'unités
- advanced_model : Modèle pour les fonctionnalités avancées
"""

# Import des modèles pour les rendre disponibles au niveau du package
from .calculator_model import CalculatorModel
from .scientific_model import ScientificCalculatorModel
from .currency_model import CurrencyModel
from .conversion_model import ConversionModel, ConversionType
from .advanced_model import AdvancedCalculatorModel

__all__ = [
    "CalculatorModel",
    "ScientificCalculatorModel",
    "CurrencyModel",
    "ConversionModel",
    "ConversionType",
    "AdvancedCalculatorModel",
]
