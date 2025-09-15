from PyQt6.QtCore import QObject
from typing import Dict, Optional, Union
import re
import math


class ScientificController(QObject):
    """
    Contrôleur pour les fonctionnalités scientifiques de la calculatrice.
    Gère les calculs scientifiques et la conversion d'unités.
    """

    # Signaux
    result_ready = pyqtSignal(str)  # Résultat du calcul
    error_occurred = pyqtSignal(str)  # Message d'erreur

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        self.view.calculate_clicked.connect(self.calculate_expression)
        self.view.unit_conversion_clicked.connect(self.convert_units)
        self.view.scientific_function_clicked.connect(self.handle_scientific_function)

    def calculate_expression(self, expression: str) -> None:
        """
        Évalue une expression mathématique.

        Args:
            expression: L'expression à évaluer
        """
        try:
            # Remplace les constantes mathématiques
            expr = expression.replace("π", "math.pi").replace("e", "math.e")

            # Gestion des fonctions trigonométriques
            if self.model.angle_mode == "DEG":
                expr = self._convert_deg_to_rad(expr)

            # Évalue l'expression de manière sécurisée
            result = str(eval(expr, {"__builtins__": None}, self._get_math_functions()))

            self.result_ready.emit(result)

        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul: {str(e)}")

    def _convert_deg_to_rad(self, expression: str) -> str:
        """Convertit les angles de degrés en radians pour les fonctions trigo"""
        trig_funcs = ["sin", "cos", "tan", "asin", "acos", "atan"]
        for func in trig_funcs:
            pattern = f"{func}\(([^)]+)\)"
            expression = re.sub(
                pattern, f"math.radians({func}(math.radians(\1)))", expression
            )
        return expression

    def _get_math_functions(self) -> Dict[str, object]:
        """Retourne un dictionnaire des fonctions mathématiques disponibles"""
        return {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e,
            "radians": math.radians,
            "degrees": math.degrees,
        }

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> None:
        """
        Convertit une valeur d'une unité à une autre.

        Args:
            value: La valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
        """
        try:
            result = self.model.convert_units(value, from_unit, to_unit)
            self.result_ready.emit(f"{value} {from_unit} = {result} {to_unit}")
        except Exception as e:
            self.error_occurred.emit(f"Erreur de conversion: {str(e)}")

    def handle_scientific_function(self, func_name: str, value: float) -> None:
        """
        Gère les fonctions scientifiques avancées.

        Args:
            func_name: Nom de la fonction à appliquer
            value: Valeur d'entrée
        """
        try:
            if func_name == "factorial":
                result = math.factorial(int(value))
            elif func_name == "sqrt":
                result = math.sqrt(value)
            elif func_name == "log10":
                result = math.log10(value)
            elif func_name == "ln":
                result = math.log(value)
            elif func_name == "exp":
                result = math.exp(value)
            else:
                raise ValueError(f"Fonction non supportée: {func_name}")

            self.result_ready.emit(f"{func_name}({value}) = {result}")

        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul: {str(e)}")
