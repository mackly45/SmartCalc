import numpy as np
import sympy as sp
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime


class AdvancedCalculatorModel(QObject):
    """Modèle pour la calculatrice avancée (graphiques, matrices, factorisation)"""

    # Signaux
    plot_updated = pyqtSignal(np.ndarray, np.ndarray)  # x, y
    matrix_operation_completed = pyqtSignal(np.ndarray)  # result_matrix
    factorization_completed = pyqtSignal(str)  # result_expression
    error_occurred = pyqtSignal(str)  # error_message

    def __init__(self):
        super().__init__()
        self.history = []
        self.max_history = 100

        # État actuel
        self.current_plot = None
        self.current_matrix_a = None
        self.current_matrix_b = None
        self.current_expression = ""

    # Méthodes pour les graphiques
    def plot_function(self, expression, x_min, x_max, num_points=1000):
        """Évalue une fonction mathématique pour le tracé"""
        try:
            x = np.linspace(x_min, x_max, num_points)

            # Créer un environnement d'évaluation sécurisé
            safe_env = {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "arcsin": np.arcsin,
                "arccos": np.arccos,
                "arctan": np.arctan,
                "sinh": np.sinh,
                "cosh": np.cosh,
                "tanh": np.tanh,
                "exp": np.exp,
                "log": np.log,
                "log10": np.log10,
                "sqrt": np.sqrt,
                "abs": np.abs,
                "pi": np.pi,
                "e": np.e,
            }

            # Évaluer l'expression
            y = eval(expression, {"__builtins__": {}}, safe_env)

            # Vérifier les résultats valides
            if np.any(np.isnan(y)) or np.any(np.isinf(y)):
                self.error_occurred.emit(
                    "La fonction génère des valeurs non numériques"
                )
                return

            self.current_plot = (x, y)
            self.plot_updated.emit(x, y)

        except Exception as e:
            self.error_occurred.emit(f"Erreur lors du tracé: {str(e)}")

    # Méthodes pour les matrices
    def set_matrix_a(self, matrix):
        """Définit la matrice A"""
        self.current_matrix_a = np.array(matrix, dtype=float)

    def set_matrix_b(self, matrix):
        """Définit la matrice B"""
        self.current_matrix_b = np.array(matrix, dtype=float)

    def add_matrices(self):
        """Additionne deux matrices"""
        try:
            if self.current_matrix_a is None or self.current_matrix_b is None:
                raise ValueError("Les deux matrices doivent être définies")

            if self.current_matrix_a.shape != self.current_matrix_b.shape:
                raise ValueError("Les matrices doivent avoir les mêmes dimensions")

            result = self.current_matrix_a + self.current_matrix_b
            self.matrix_operation_completed.emit(result)

        except Exception as e:
            self.error_occurred.emit(f"Erreur d'addition matricielle: {str(e)}")

    def multiply_matrices(self):
        """Multiplie deux matrices"""
        try:
            if self.current_matrix_a is None or self.current_matrix_b is None:
                raise ValueError("Les deux matrices doivent être définies")

            if self.current_matrix_a.shape[1] != self.current_matrix_b.shape[0]:
                raise ValueError(
                    "Le nombre de colonnes de A doit être égal au nombre de lignes de B"
                )

            result = np.dot(self.current_matrix_a, self.current_matrix_b)
            self.matrix_operation_completed.emit(result)

        except Exception as e:
            self.error_occurred.emit(f"Erreur de multiplication matricielle: {str(e)}")

    def calculate_determinant(self, matrix):
        """Calcule le déterminant d'une matrice"""
        try:
            if matrix is None:
                raise ValueError("Aucune matrice définie")

            if matrix.shape[0] != matrix.shape[1]:
                raise ValueError("La matrice doit être carrée")

            return np.linalg.det(matrix)

        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul du déterminant: {str(e)}")
            return None

    def calculate_inverse(self, matrix):
        """Calcule l'inverse d'une matrice"""
        try:
            if matrix is None:
                raise ValueError("Aucune matrice définie")

            if matrix.shape[0] != matrix.shape[1]:
                raise ValueError("La matrice doit être carrée")

            det = self.calculate_determinant(matrix)
            if det == 0:
                raise ValueError("La matrice n'est pas inversible (déterminant nul)")

            return np.linalg.inv(matrix)

        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul de l'inverse: {str(e)}")
            return None

    # Méthodes pour la factorisation
    def factor_expression(self, expression):
        """Factorise une expression mathématique"""
        try:
            x = sp.Symbol("x")
            expr = sp.sympify(expression)
            factored = sp.factor(expr)

            # Vérifier si la factorisation a fonctionné
            if sp.expand(factored) != sp.expand(expr):
                self.error_occurred.emit(
                    "Impossible de factoriser complètement l'expression"
                )
                return None

            return str(factored)

        except Exception as e:
            self.error_occurred.emit(f"Erreur de factorisation: {str(e)}")
            return None

    def analyze_expression(self, expression):
        """Analyse une expression mathématique (racines, dérivée, etc.)"""
        try:
            x = sp.Symbol("x")
            expr = sp.sympify(expression)

            # Calculer la dérivée
            derivative = sp.diff(expr, x)

            # Trouver les racines
            roots = sp.solve(expr, x)

            # Trouver les points critiques (où la dérivée s'annule)
            critical_points = sp.solve(derivative, x)

            return {
                "derivative": str(derivative),
                "roots": [str(r) for r in roots],
                "critical_points": [str(cp) for cp in critical_points],
            }

        except Exception as e:
            self.error_occurred.emit(f"Erreur d'analyse: {str(e)}")
            return None

    # Gestion de l'historique
    def add_to_history(self, operation, params, result):
        """Ajoute une opération à l'historique"""
        entry = {
            "timestamp": datetime.now(),
            "operation": operation,
            "params": params,
            "result": result,
        }

        self.history.append(entry)

        # Limiter la taille de l'historique
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def clear_history(self):
        """Efface l'historique"""
        self.history = []

    def get_history(self, limit=None):
        """Récupère l'historique"""
        if limit is not None and limit > 0:
            return self.history[-limit:]
        return self.history.copy()
