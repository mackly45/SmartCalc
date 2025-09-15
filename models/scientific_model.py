import math
import cmath
import re
from datetime import datetime
from typing import Union, List, Tuple, Optional


class ScientificCalculatorModel:
    """
    Modèle pour la calculatrice scientifique.
    Gère les calculs scientifiques et l'historique.
    """

    def __init__(self):
        self.memory = 0
        self.last_ans = 0
        self.angle_mode = "DEG"  # DEG, RAD, GRAD
        self.history = []
        self.max_history_size = 100
        self.settings = {
            "angle_mode": "DEG",
            "number_format": "normal",  # normal, sci, eng
            "precision": 10,
        }

    def set_angle_mode(self, mode: str) -> bool:
        """
        Définit le mode d'angle.

        Args:
            mode: 'DEG', 'RAD' ou 'GRAD'

        Returns:
            bool: True si le mode a été changé, False sinon
        """
        mode = mode.upper()
        if mode in ["DEG", "RAD", "GRAD"]:
            self.settings["angle_mode"] = mode
            self.angle_mode = mode
            return True
        return False

    def to_radians(self, angle: float) -> float:
        """
        Convertit un angle en radians selon le mode actuel.

        Args:
            angle: L'angle à convertir

        Returns:
            float: L'angle en radians
        """
        if self.settings["angle_mode"] == "DEG":
            return math.radians(angle)
        elif self.settings["angle_mode"] == "GRAD":
            return angle * math.pi / 200
        return angle  # Déjà en radians

    def from_radians(self, angle: float) -> float:
        """
        Convertit des radians vers le mode d'angle actuel.

        Args:
            angle: L'angle en radians

        Returns:
            float: L'angle converti
        """
        if self.settings["angle_mode"] == "DEG":
            return math.degrees(angle)
        elif self.settings["angle_mode"] == "GRAD":
            return angle * 200 / math.pi
        return angle  # Déjà dans le bon mode

    def evaluate_expression(self, expression: str) -> float:
        """
        Évalue une expression mathématique.

        Args:
            expression: L'expression à évaluer

        Returns:
            float: Le résultat du calcul

        Raises:
            ValueError: Si l'expression est invalide
        """
        try:
            # Remplacer les constantes
            expr = expression.replace("π", "pi").replace("e", "math.e")

            # Remplacer les fonctions trigonométriques avec gestion du mode angle
            if self.settings["angle_mode"] != "RAD":
                for func in ["sin", "cos", "tan", "asin", "acos", "atan"]:
                    expr = re.sub(
                        rf"({func})\(([^)]+)\)",
                        rf"math.{func}(self.to_radians(\2))",
                        expr,
                    )
            else:
                for func in ["sin", "cos", "tan", "asin", "acos", "atan"]:
                    expr = expr.replace(f"{func}(", f"math.{func}(")

            # Remplacer les autres fonctions mathématiques
            math_funcs = ["sqrt", "log", "log10", "exp", "factorial", "gamma", "log2"]
            for func in math_funcs:
                expr = expr.replace(f"{func}(", f"math.{func}(")

            # Remplacer les fonctions hyperboliques
            hyp_funcs = ["sinh", "cosh", "tanh", "asinh", "acosh", "atanh"]
            for func in hyp_funcs:
                expr = expr.replace(f"{func}(", f"math.{func}(")

            # Évaluer l'expression
            result = eval(
                expr,
                {"__builtins__": None},
                {
                    "math": math,
                    "e": math.e,
                    "pi": math.pi,
                    "ans": self.last_ans,
                    "sqrt": math.sqrt,
                    "log": math.log10,
                    "ln": math.log,
                    "exp": math.exp,
                    "abs": abs,
                    "round": round,
                    "floor": math.floor,
                    "ceil": math.ceil,
                    "sin": (
                        math.sin
                        if self.settings["angle_mode"] == "RAD"
                        else lambda x: math.sin(self.to_radians(x))
                    ),
                    "cos": (
                        math.cos
                        if self.settings["angle_mode"] == "RAD"
                        else lambda x: math.cos(self.to_radians(x))
                    ),
                    "tan": (
                        math.tan
                        if self.settings["angle_mode"] == "RAD"
                        else lambda x: math.tan(self.to_radians(x))
                    ),
                    "asin": lambda x: (
                        self.from_radians(math.asin(x))
                        if self.settings["angle_mode"] != "RAD"
                        else math.asin(x)
                    ),
                    "acos": lambda x: (
                        self.from_radians(math.acos(x))
                        if self.settings["angle_mode"] != "RAD"
                        else math.acos(x)
                    ),
                    "atan": lambda x: (
                        self.from_radians(math.atan(x))
                        if self.settings["angle_mode"] != "RAD"
                        else math.atan(x)
                    ),
                    "sinh": math.sinh,
                    "cosh": math.cosh,
                    "tanh": math.tanh,
                    "asinh": math.asinh,
                    "acosh": math.acosh,
                    "atanh": math.atanh,
                    "log10": math.log10,
                    "log2": math.log2,
                    "factorial": math.factorial,
                    "gcd": math.gcd,
                    "degrees": math.degrees,
                    "radians": math.radians,
                    "mod": lambda x, y: x % y,
                    "comb": (
                        math.comb
                        if hasattr(math, "comb")
                        else lambda n, k: math.factorial(n)
                        // (math.factorial(k) * math.factorial(n - k))
                    ),
                    "perm": lambda n, k: (
                        math.perm(int(n), int(k))
                        if hasattr(math, "perm")
                        else math.factorial(n) // math.factorial(int(n) - int(k))
                    ),
                    "gamma": math.gamma,
                    "lgamma": math.lgamma,
                    "erf": math.erf,
                    "erfc": math.erfc,
                    "isqrt": (
                        math.isqrt
                        if hasattr(math, "isqrt")
                        else lambda x: int(math.sqrt(x))
                    ),
                    "isclose": math.isclose,
                    "lcm": lambda a, b: (
                        abs(a * b) // math.gcd(int(a), int(b)) if a and b else 0
                    ),
                    "j": 1j,
                    "complex": complex,
                    "polar": cmath.polar,
                    "rect": cmath.rect,
                    "phase": cmath.phase,
                    "polar_to_rect": lambda r, phi: (
                        r * math.cos(phi),
                        r * math.sin(phi),
                    ),
                    "rect_to_polar": lambda x, y: cmath.polar(complex(x, y)),
                },
            )

            self.last_ans = result
            self.add_to_history(expression, result)
            return result

        except Exception as e:
            raise ValueError(f"Erreur d'évaluation: {str(e)}")

    def add_to_history(self, expression: str, result: float) -> None:
        """
        Ajoute un calcul à l'historique.

        Args:
            expression: L'expression calculée
            result: Le résultat du calcul
        """
        timestamp = datetime.now()
        self.history.append(
            {
                "timestamp": timestamp,
                "expression": expression,
                "result": result,
                "mode": self.settings["angle_mode"],
            }
        )

        # Limiter la taille de l'historique
        if len(self.history) > self.max_history_size:
            self.history.pop(0)

    def get_history(self) -> List[dict]:
        """
        Retourne l'historique des calculs.

        Returns:
            List[dict]: La liste des calculs effectués
        """
        return self.history

    def clear_history(self) -> None:
        """Efface l'historique des calculs."""
        self.history = []

    def memory_add(self, value: float) -> None:
        """
        Ajoute une valeur à la mémoire.

        Args:
            value: La valeur à ajouter
        """
        self.memory += value

    def memory_subtract(self, value: float) -> None:
        """
        Soustrait une valeur de la mémoire.

        Args:
            value: La valeur à soustraire
        """
        self.memory -= value

    def memory_recall(self) -> float:
        """
        Récupère la valeur en mémoire.

        Returns:
            float: La valeur en mémoire
        """
        return self.memory

    def memory_clear(self) -> None:
        """Réinitialise la mémoire à zéro."""
        self.memory = 0

    def get_angle_mode(self) -> str:
        """
        Retourne le mode d'angle actuel.

        Returns:
            str: Le mode d'angle ('DEG', 'RAD' ou 'GRAD')
        """
        return self.settings["angle_mode"]

    def set_precision(self, precision: int) -> None:
        """
        Définit la précision des calculs.

        Args:
            precision: Le nombre de décimales à afficher
        """
        if 0 <= precision <= 15:
            self.settings["precision"] = precision

    def get_precision(self) -> int:
        """
        Retourne la précision actuelle.

        Returns:
            int: Le nombre de décimales affichées
        """
        return self.settings["precision"]
