"""
Package contenant les vues de l'application SmartCalc.

Ce package inclut les vues suivantes :
- calculator_view : Vue pour la calculatrice de base
- scientific_view : Vue pour les fonctions scientifiques
- currency_view : Vue pour la conversion de devises
- conversion_view : Vue pour la conversion d'unités
- advanced_view : Vue pour les fonctionnalités avancées
"""

# Import des vues pour les rendre disponibles au niveau du package
from .calculator_view import CalculatorView
from .scientific_view import ScientificView
from .currency_view import CurrencyView
from .conversion_view import ConversionView
from .advanced_view import AdvancedView

__all__ = [
    "CalculatorView",
    "ScientificView",
    "CurrencyView",
    "ConversionView",
    "AdvancedView",
]
