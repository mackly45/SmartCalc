from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol, diff, integrate, solve, limit, oo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas


class AdvancedController(QObject):
    """
    Contrôleur pour les fonctionnalités avancées de la calculatrice.
    Gère les opérations avancées comme les calculs symboliques.
    """

    # Signaux
    calculation_complete = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)
    graph_updated = pyqtSignal(QPixmap)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur."""
        self.view.calculate_clicked.connect(self.calculate_expression)
        self.view.plot_clicked.connect(self.plot_function)
        self.view.solve_clicked.connect(self.solve_equation)
        self.view.differentiate_clicked.connect(self.differentiate_expression)
        self.view.integrate_clicked.connect(self.integrate_expression)
        self.view.limit_clicked.connect(self.calculate_limit)
        self.view.series_clicked.connect(self.calculate_series)

    def calculate_expression(self, expression, variables):
        """Calcule le résultat d'une expression mathématique."""
        try:
            result = self.model.evaluate_expression(expression, variables)
            self.calculation_complete.emit(expression, str(result))
        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul: {str(e)}")

    def plot_function(self, expression, x_range, y_range):
        """Trace le graphe d'une fonction."""
        try:
            x = np.linspace(x_range[0], x_range[1], 400)
            y = self.model.evaluate_expression(expression, {"x": x})

            # Création de la figure
            fig, ax = plt.subplots()
            ax.plot(x, y)

            # Configuration du graphe
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"Graphe de {expression}")
            ax.grid(True)

            # Conversion en QPixmap
            canvas = FigureCanvas(fig)
            canvas.draw()

            # Création d'un QPixmap à partir de la figure
            width, height = fig.get_size_inches() * fig.get_dpi()
            pixmap = QPixmap(int(width), int(height))
            pixmap.fill()

            # Sauvegarde de la figure dans le QPixmap
            fig.savefig("temp_plot.png")
            pixmap = QPixmap("temp_plot.png")

            # Émission du signal avec le graphe
            self.graph_updated.emit(pixmap)

        except Exception as e:
            self.error_occurred.emit(f"Erreur lors du tracé: {str(e)}")

    def solve_equation(self, equation, variable):
        """Résout une équation pour une variable donnée."""
        try:
            solution = self.model.solve_equation(equation, variable)
            self.calculation_complete.emit(
                f"Résolution de {equation} pour {variable}", f"Solution: {solution}"
            )
        except Exception as e:
            self.error_occurred.emit(f"Erreur de résolution: {str(e)}")

    def differentiate_expression(self, expression, variable, order=1):
        """Calcule la dérivée d'une expression."""
        try:
            derivative = self.model.differentiate(expression, variable, order)
            self.calculation_complete.emit(
                f"Dérivée d'ordre {order} de {expression} par rapport à {variable}",
                f"Résultat: {derivative}",
            )
        except Exception as e:
            self.error_occurred.emit(f"Erreur de dérivation: {str(e)}")

    def integrate_expression(self, expression, variable, lower=None, upper=None):
        """Calcule l'intégrale d'une expression."""
        try:
            if lower is not None and upper is not None:
                # Intégrale définie
                result = self.model.definite_integrate(
                    expression, variable, float(lower), float(upper)
                )
                self.calculation_complete.emit(
                    f"Intégrale de {expression} de {lower} à {upper} par rapport à {variable}",
                    f"Résultat: {result}",
                )
            else:
                # Intégrale indéfinie
                result = self.model.indefinite_integrate(expression, variable)
                self.calculation_complete.emit(
                    f"Primitive de {expression} par rapport à {variable}",
                    f"Résultat: {result} + C",
                )
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'intégration: {str(e)}")

    def calculate_limit(self, expression, variable, point, direction):
        """Calcule la limite d'une expression."""
        try:
            lim = self.model.calculate_limit(expression, variable, point, direction)
            self.calculation_complete.emit(
                f"Limite de {expression} quand {variable} -> {point}{'⁻' if direction == '-' else ''}",
                f"Résultat: {lim}",
            )
        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul de limite: {str(e)}")

    def calculate_series(self, expression, variable, point, order):
        """Calcule le développement en série d'une expression."""
        try:
            series = self.model.series_expansion(expression, variable, point, order)
            self.calculation_complete.emit(
                f"Développement en série de {expression} autour de {point} à l'ordre {order}",
                f"Résultat: {series}",
            )
        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul de série: {str(e)}")
