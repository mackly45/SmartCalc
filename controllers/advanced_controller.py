from PyQt6.QtCore import QObject
from PyQt6.QtGui import QPixmap
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol, diff, integrate, solve, limit, oo
from typing import Dict, Optional, Tuple, Union
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas


class AdvancedController(QObject):
    """
    Contrôleur pour les fonctionnalités avancées de la calculatrice.
    Gère les opérations avancées comme les calculs symboliques, les graphiques, etc.
    """

    # Signaux
    calculation_complete = QObject().pyqtSignal(str, str)  # expression, résultat
    error_occurred = QObject().pyqtSignal(str)  # message d'erreur
    graph_updated = QObject().pyqtSignal(QPixmap)  # image du graphique

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        self.view.calculate_clicked.connect(self.calculate_expression)
        self.view.plot_clicked.connect(self.plot_expression)
        self.view.solve_clicked.connect(self.solve_equation)
        self.view.differentiate_clicked.connect(self.differentiate_expression)
        self.view.integrate_clicked.connect(self.integrate_expression)
        self.view.limit_clicked.connect(self.calculate_limit)
        self.view.series_clicked.connect(self.calculate_series)

    def calculate_expression(
        self, expression: str, variables: Dict[str, float]
    ) -> None:
        """
        Calcule la valeur d'une expression avec les variables fournies.

        Args:
            expression: L'expression à évaluer
            variables: Dictionnaire des variables et leurs valeurs
        """
        try:
            for var, val in variables.items():
                expression = expression.replace(var, str(val))

            result = str(
                eval(
                    expression,
                    {"__builtins__": None},
                    {
                        "sin": np.sin,
                        "cos": np.cos,
                        "tan": np.tan,
                        "exp": np.exp,
                        "log": np.log,
                        "sqrt": np.sqrt,
                        "pi": np.pi,
                        "e": np.e,
                        "j": 1j,
                    },
                )
            )

            self.calculation_complete.emit(expression, result)

        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul: {str(e)}")

    def plot_expression(
        self,
        expression: str,
        x_range: Tuple[float, float],
        y_range: Optional[Tuple[float, float]] = None,
    ) -> None:
        """
        Trace le graphe d'une expression mathématique.

        Args:
            expression: L'expression à tracer
            x_range: Tuple (min, max) pour l'axe des x
            y_range: Optionnel, tuple (min, max) pour l'axe des y
        """
        try:
            x = np.linspace(x_range[0], x_range[1], 1000)
            y = eval(
                expression,
                {"__builtins__": None},
                {
                    "x": x,
                    "sin": np.sin,
                    "cos": np.cos,
                    "tan": np.tan,
                    "exp": np.exp,
                    "log": np.log,
                    "sqrt": np.sqrt,
                    "pi": np.pi,
                    "e": np.e,
                },
            )

            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"Graphe de {expression}")

            if y_range:
                ax.set_ylim(y_range)

            canvas = FigureCanvas(fig)
            pixmap = QPixmap(canvas.size())
            canvas.render(pixmap)
            self.graph_updated.emit(pixmap)

        except Exception as e:
            self.error_occurred.emit(f"Erreur lors du tracé: {str(e)}")

    def solve_equation(self, equation: str, variable: str = "x") -> None:
        """
        Résout une équation symbolique.

        Args:
            equation: L'équation à résoudre (ex: "x**2 - 1 = 0")
            variable: La variable à résoudre (par défaut: 'x')
        """
        try:
            eq = equation.replace("=", "-")
            sympy_eq = parse_expr(eq)
            solution = solve(sympy_eq, Symbol(variable))

            self.calculation_complete.emit(
                f"Résolution de {equation}", f"Solution: {solution}"
            )

        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de la résolution: {str(e)}")

    def differentiate_expression(
        self, expression: str, variable: str = "x", order: int = 1
    ) -> None:
        """
        Calcule la dérivée d'une expression.

        Args:
            expression: L'expression à dériver
            variable: La variable de dérivation (par défaut: 'x')
            order: Ordre de dérivation (par défaut: 1)
        """
        try:
            expr = parse_expr(expression)
            derivative = diff(expr, Symbol(variable), order)

            self.calculation_complete.emit(
                f"Dérivée d'ordre {order} de {expression} par rapport à " f"{variable}",
                f"Résultat: {derivative}",
            )

        except Exception as e:
            msg = f"Erreur lors du calcul de la dérivée: {str(e)}"
            self.error_occurred.emit(msg)

    def integrate_expression(
        self,
        expression: str,
        variable: str = "x",
        lower: Optional[float] = None,
        upper: Optional[float] = None,
    ) -> None:
        """
        Calcule l'intégrale d'une expression.

        Args:
            expression: L'expression à intégrer
            variable: Variable d'intégration (par défaut: 'x')
            lower: Borne inférieure (intégrale définie si fournie)
            upper: Borne supérieure (intégrale définie si fournie)
        """
        try:
            expr = parse_expr(expression)

            if lower is not None and upper is not None:
                result = integrate(expr, (Symbol(variable), lower, upper))
                result_str = f"de {lower} à {upper}: {result}"
            else:
                result = integrate(expr, Symbol(variable))
                result_str = f"{result} + C"

            self.calculation_complete.emit(
                f"Intégrale de {expression}", f"Résultat: {result_str}"
            )

        except Exception as e:
            msg = f"Erreur lors du calcul de l'intégrale: {str(e)}"
            self.error_occurred.emit(msg)

    def calculate_limit(
        self,
        expression: str,
        variable: str,
        point: Union[float, str],
        direction: str = "+",
    ) -> None:
        """
        Calcule la limite d'une expression.

        Args:
            expression: L'expression dont on veut la limite
            variable: La variable de la limite
            point: Le point vers lequel tend la variable
            direction: '+' pour la limite à droite, '-' pour la limite à gauche
        """
        try:
            expr = parse_expr(expression)
            limit_point = oo if point == "oo" else point
            lim = limit(expr, Symbol(variable), limit_point, dir=direction)

            self.calculation_complete.emit(
                f"Limite de {expression} quand {variable} -> {point}{direction}",
                f"Résultat: {lim}",
            )

        except Exception as e:
            msg = f"Erreur lors du calcul de la limite: {str(e)}"
            self.error_occurred.emit(msg)

    def calculate_series(
        self, expression: str, variable: str, point: float = 0, order: int = 5
    ) -> None:
        """
        Calcule le développement en série d'une expression.

        Args:
            expression: L'expression à développer
            variable: La variable du développement
            point: Point autour duquel effectuer le développement
            order: Ordre du développement
        """
        try:
            expr = parse_expr(expression)
            series = expr.series(Symbol(variable), point, order).removeO()

            self.calculation_complete.emit(
                f"Développement en série de {expression} autour de {point}",
                f"Résultat: {series}",
            )

        except Exception as e:
            msg = f"Erreur lors du calcul du développement en série: {str(e)}"
            self.error_occurred.emit(msg)
