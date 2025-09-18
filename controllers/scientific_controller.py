from PyQt6.QtCore import QObject, pyqtSignal
import math


class ScientificController(QObject):
    """
    Contrôleur pour les opérations scientifiques.
    Gère les calculs avancés comme les fonctions trigonométriques.
    """

    # Signaux
    calculation_complete = pyqtSignal(str, str)  # expression, résultat
    error_occurred = pyqtSignal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.angle_unit = "DEG"  # DEG, RAD, GRAD
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur."""
        self.view.button_clicked.connect(self.on_button_clicked)
        self.view.function_clicked.connect(self.on_function_clicked)
        self.view.angle_unit_changed.connect(self.set_angle_unit)
        self.view.calculate_clicked.connect(self.calculate_expression)

    def set_angle_unit(self, unit):
        """Définit l'unité d'angle à utiliser."""
        self.angle_unit = unit

    def on_button_clicked(self, button_text):
        """Gère le clic sur un bouton de la calculatrice."""
        if button_text == "C":
            self.view.clear_display()
        elif button_text == "⌫":
            self.view.backspace()
        elif button_text == "±":
            self.view.toggle_sign()
        elif button_text == "=":
            self.calculate_expression()
        else:
            # Ajoute le texte du bouton à l'affichage
            self.view.append_to_display(button_text)

    def _convert_input_angle(self, value: float) -> float:
        """Convertit la valeur en radians selon l'unité courante (pour sin/cos/tan)."""
        if self.angle_unit == "DEG":
            return math.radians(value)
        if self.angle_unit == "GRAD":
            return math.radians(value * 0.9)
        return value  # RAD

    def _convert_output_angle(self, value: float) -> float:
        """Convertit le résultat des fonctions inverses selon l'unité courante."""
        if self.angle_unit == "DEG":
            return math.degrees(value)
        if self.angle_unit == "GRAD":
            return math.degrees(value) * 10 / 9
        return value

    def on_function_clicked(self, function_name):
        """Gère le clic sur une fonction scientifique (refactorée pour réduire la complexité)."""
        current_text = self.view.get_display_text()
        try:
            # Fonctions à un argument numérique simple
            unary_numeric = {
                "log": lambda x: math.log10(x),
                "ln": lambda x: math.log(x),
                "exp": lambda x: math.exp(x),
                "x²": lambda x: x**2,
                "√": lambda x: math.sqrt(x),
                "π": lambda _: math.pi,
                "e": lambda _: math.e,
                "x!": lambda x: math.factorial(int(float(x))),
            }

            if function_name in ("sin", "cos", "tan"):
                value = float(current_text)
                value = self._convert_input_angle(value)
                funcs = {"sin": math.sin, "cos": math.cos, "tan": math.tan}
                result = funcs[function_name](value)
                self.view.set_display_text(str(result))
                return

            if function_name in ("asin", "acos", "atan"):
                value = float(current_text)
                funcs = {"asin": math.asin, "acos": math.acos, "atan": math.atan}
                result = funcs[function_name](value)
                result = self._convert_output_angle(result)
                self.view.set_display_text(str(result))
                return

            if function_name in unary_numeric:
                x = float(current_text) if current_text not in ("π", "e") else None
                result = unary_numeric[function_name](x) if x is not None else unary_numeric[function_name](0)
                self.view.set_display_text(str(result))
                return

            if function_name == "x^y":
                # Ajoute l'opérateur de puissance et attend la seconde entrée
                self.view.append_to_display("^")
                return

            # Si la fonction n'est pas reconnue
            raise ValueError(f"Fonction inconnue: {function_name}")

        except Exception as e:
            self.error_occurred.emit(f"Erreur de calcul: {str(e)}")

    def calculate_expression(self):
        """Évalue l'expression mathématique actuelle."""
        try:
            expression = self.view.get_display_text()

            # Remplace les symboles spéciaux
            expression = expression.replace("^", "**")

            # Crée un dictionnaire de fonctions et constantes disponibles
            math_funcs = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "log": math.log10,
                "ln": math.log,
                "exp": math.exp,
                "sqrt": math.sqrt,
                "pi": math.pi,
                "e": math.e,
                "radians": math.radians,
                "degrees": math.degrees,
            }

            # Évalue l'expression de manière sécurisée
            result = eval(expression, {"__builtins__": None}, math_funcs)

            # Affiche le résultat
            self.view.set_display_text(str(result))

        except Exception as e:
            self.error_occurred.emit(f"Erreur d'expression: {str(e)}")

    def show_error(self, message):
        """Affiche un message d'erreur."""
        self.error_occurred.emit(message)

    # Harmonisation avec main.py
    def initialize_ui(self):
        """Initialise l'onglet scientifique (état par défaut)."""
        # Par défaut on remet l'unité d'angle à DEG et on efface l'affichage
        self.set_angle_unit("DEG")
        if hasattr(self.view, 'clear_display'):
            self.view.clear_display()

    def cleanup(self):
        """Nettoyage des ressources (aucune pour le moment)."""
        pass
