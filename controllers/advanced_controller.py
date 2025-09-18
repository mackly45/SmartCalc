from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


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

        # Option A: relier les signaux du contrôleur à la vue pour affichage auto
        self.calculation_complete.connect(
            lambda expr, res: getattr(self.view, 'show_result', lambda *_: None)(res)
        )
        self.error_occurred.connect(
            lambda msg: getattr(self.view, 'show_error', lambda *_: None)(msg)
        )
        # graph_updated envoie un QPixmap; la vue trace déjà via Matplotlib.
        # On privilégie l'appel direct à view.plot_function dans plot_function().

    def calculate_expression(self, expression, variables):
        """Calcule le résultat d'une expression mathématique."""
        try:
            result = self.model.evaluate_expression(expression, variables)
            self.calculation_complete.emit(expression, str(result))
            # Option B: appel direct de la vue
            if hasattr(self.view, 'show_result'):
                self.view.show_result(str(result))
        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul: {str(e)}")

    def plot_function(self, expression, x_range, y_range):
        """Trace le graphe d'une fonction."""
        try:
            x = np.linspace(x_range[0], x_range[1], 400)
            y = self.model.evaluate_expression(expression, {"x": x})

            # Option B: demander à la vue de tracer directement (matplotlib embarqué)
            if hasattr(self.view, 'plot_function'):
                try:
                    self.view.plot_function(x, y, expression)
                except Exception:
                    pass
            else:
                # Fallback: créer une figure et sauvegarder (peu utilisé désormais)
                fig, ax = plt.subplots()
                ax.plot(x, y)
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                ax.set_title(f"Graphe de {expression}")
                ax.grid(True)
                canvas = FigureCanvas(fig)
                canvas.draw()
                width, height = fig.get_size_inches() * fig.get_dpi()
                pixmap = QPixmap(int(width), int(height))
                pixmap.fill()
                fig.savefig("temp_plot.png")
                pixmap = QPixmap("temp_plot.png")
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
            # Option B: appel direct
            if hasattr(self.view, 'show_result'):
                self.view.show_result(f"Solution: {solution}")
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
            # Option B: appel direct spécifique
            if hasattr(self.view, 'show_derivative_result'):
                self.view.show_derivative_result(str(derivative))
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
                    f"Intégrale de {expression} de {lower} à {upper} "
                    f"par rapport à {variable}",
                    f"Résultat: {result}",
                )
                if hasattr(self.view, 'show_integral_result'):
                    self.view.show_integral_result(str(result))
            else:
                # Intégrale indéfinie
                result = self.model.indefinite_integrate(expression, variable)
                self.calculation_complete.emit(
                    f"Primitive de {expression} par rapport à {variable}",
                    f"Résultat: {result} + C",
                )
                if hasattr(self.view, 'show_integral_result'):
                    self.view.show_integral_result(f"{result} + C")
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'intégration: {str(e)}")

    def calculate_limit(self, expression, variable, point, direction):
        """Calcule la limite d'une expression."""
        try:
            lim = self.model.calculate_limit(expression, variable, point, direction)
            self.calculation_complete.emit(
                f"Limite de {expression} quand {variable} -> "
                f"{point}{'⁻' if direction == '-' else ''}",
                f"Résultat: {lim}",
            )
            if hasattr(self.view, 'show_limit_result'):
                self.view.show_limit_result(str(lim))
        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul de limite: {str(e)}")

    def calculate_series(self, expression, variable, point, order):
        """Calcule le développement en série d'une expression."""
        try:
            series = self.model.series_expansion(expression, variable, point, order)
            self.calculation_complete.emit(
                f"Développement en série de {expression} "
                f"autour de {point} à l'ordre {order}",
                f"Résultat: {series}",
            )
            if hasattr(self.view, 'show_series_result'):
                self.view.show_series_result(str(series))
        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul de série: {str(e)}")

    # Harmonisation avec main.py
    def initialize_ui(self):
        """Initialise l'onglet avancé (réinitialisation de l'état)."""
        # Si la vue possède des méthodes de reset, on peut les appeler ici.
        if hasattr(self.view, 'clear'):
            try:
                self.view.clear()
            except Exception:
                pass

    def cleanup(self):
        """Nettoyage des ressources de l'onglet avancé."""
        # Rien de spécifique pour le moment.
        pass
