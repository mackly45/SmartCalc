import math
from typing import Dict, Optional, List


class ScientificModel:
    """
    Modèle pour les opérations scientifiques de la calculatrice.
    Gère les calculs mathématiques avancés.
    """

    def __init__(self):
        self.history = []
        self.memory = 0.0
        self.angle_mode = "DEG"  # DEG, RAD, GRAD

    def evaluate_expression(
        self, expression: str, variables: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Évalue une expression mathématique.

        Args:
            expression: L'expression à évaluer
            variables: Dictionnaire des variables et leurs valeurs

        Returns:
            Le résultat de l'évaluation
        """
        try:
            # Crée un espace de noms sécurisé pour l'évaluation
            safe_dict = {
                "__builtins__": None,
                "math": math,
                "sin": self._wrap_angle_math(math.sin),
                "cos": self._wrap_angle_math(math.cos),
                "tan": self._wrap_angle_math(math.tan),
                "asin": self._wrap_angle_math(math.asin, inverse=True),
                "acos": self._wrap_angle_math(math.acos, inverse=True),
                "atan": self._wrap_angle_math(math.atan, inverse=True),
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "round": round,
                "int": int,
                "float": float,
            }

            # Ajoute les variables à l'espace de noms
            if variables:
                safe_dict.update(variables)

            # Évalue l'expression de manière sécurisée
            result = eval(expression, {"__builtins__": None}, safe_dict)

            # Ajoute à l'historique
            self.history.append(
                {
                    "expression": expression,
                    "result": result,
                    "variables": variables or {},
                }
            )

            return float(result)

        except Exception as e:
            raise ValueError(f"Erreur d'évaluation: {str(e)}")

    def _wrap_angle_math(self, func, inverse=False):
        """
        Enveloppe une fonction mathématique pour gérer les angles.

        Args:
            func: La fonction à envelopper
            inverse: Si True, c'est une fonction inverse (comme asin, acos, atan)

        Returns:
            Une fonction qui gère automatiquement les conversions d'angle
        """

        def wrapper(x):
            # Conversion avant l'application de la fonction
            if not inverse:
                if self.angle_mode == "DEG":
                    x = math.radians(x)
                elif self.angle_mode == "GRAD":
                    x = math.radians(x * 0.9)

                result = func(x)
                return result
            else:
                # Pour les fonctions inverses, on applique d'abord la fonction
                result = func(x)

                # Puis on convertit le résultat si nécessaire
                if self.angle_mode == "DEG":
                    return math.degrees(result)
                elif self.angle_mode == "GRAD":
                    return math.degrees(result) * 10 / 9
                else:  # RAD
                    return result

        return wrapper

    def set_angle_mode(self, mode: str):
        """
        Définit le mode d'angle (DEG, RAD, GRAD).

        Args:
            mode: Le mode à définir ('DEG', 'RAD' ou 'GRAD')
        """
        if mode.upper() in ["DEG", "RAD", "GRAD"]:
            self.angle_mode = mode.upper()
        else:
            raise ValueError(
                "Mode d'angle non reconnu. Utilisez 'DEG', 'RAD' ou 'GRAD'."
            )

    def memory_add(self, value: float):
        """Ajoute une valeur à la mémoire."""
        self.memory += value

    def memory_subtract(self, value: float):
        """Soustrait une valeur de la mémoire."""
        self.memory -= value

    def memory_recall(self) -> float:
        """Récupère la valeur en mémoire."""
        return self.memory

    def memory_clear(self):
        """Efface la mémoire."""
        self.memory = 0.0

    def get_history(self) -> List[Dict]:
        """
        Retourne l'historique des calculs.

        Returns:
            Liste des calculs effectués
        """
        return self.history

    def clear_history(self):
        """Efface l'historique des calculs."""
        self.history = []

    def factorial(self, n: int) -> int:
        """
        Calcule la factorielle d'un nombre entier positif.

        Args:
            n: L'entier dont on veut calculer la factorielle

        Returns:
            La factorielle de n
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError(
                "La factorielle n'est définie que pour les entiers positifs"
            )
        return math.factorial(n)

    def permutation(self, n: int, k: int) -> int:
        """
        Calcule le nombre de permutations de k éléments parmi n.

        Args:
            n: Nombre total d'éléments
            k: Nombre d'éléments à sélectionner

        Returns:
            Le nombre de permutations
        """
        if n < 0 or k < 0 or k > n:
            return 0
        return math.perm(n, k) if hasattr(math, "perm") else self._fallback_perm(n, k)

    def combination(self, n: int, k: int) -> int:
        """
        Calcule le nombre de combinaisons de k éléments parmi n.

        Args:
            n: Nombre total d'éléments
            k: Nombre d'éléments à sélectionner

        Returns:
            Le nombre de combinaisons
        """
        if n < 0 or k < 0 or k > n:
            return 0
        return math.comb(n, k) if hasattr(math, "comb") else self._fallback_comb(n, k)

    def _fallback_perm(self, n: int, k: int) -> int:
        """Implémentation de remplacement pour math.perm"""
        if k == 0:
            return 1
        return n * self._fallback_perm(n - 1, k - 1)

    def _fallback_comb(self, n: int, k: int) -> int:
        """Implémentation de remplacement pour math.comb"""
        if k == 0 or k == n:
            return 1
        return self._fallback_comb(n - 1, k - 1) + self._fallback_comb(n - 1, k)


# --- Compatibilité rétroactive pour l'ancienne classe attendue par certains tests/anciens imports ---
class ScientificCalculatorModel(ScientificModel):
    """Alias conservé pour compatibilité avec d'anciens imports/tests."""
    pass
