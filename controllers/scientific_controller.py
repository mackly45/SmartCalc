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
        current = self.view.get_display_text()

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

    def on_function_clicked(self, function_name):
        """Gère le clic sur une fonction scientifique."""
        current = self.view.get_display_text()

        try:
            if function_name in ["sin", "cos", "tan", "asin", "acos", "atan"]:
                # Gestion des fonctions trigonométriques
                value = float(current)

                # Conversion en radians si nécessaire
                if self.angle_unit == "DEG":
                    value = math.radians(value)
                elif self.angle_unit == "GRAD":
                    value = math.radians(value * 0.9)

                # Application de la fonction
                if function_name == "sin":
                    result = math.sin(value)
                elif function_name == "cos":
                    result = math.cos(value)
                elif function_name == "tan":
                    result = math.tan(value)
                elif function_name == "asin":
                    result = math.asin(value)
                    # Conversion inverse pour l'affichage
                    if self.angle_unit == "DEG":
                        result = math.degrees(result)
                    elif self.angle_unit == "GRAD":
                        result = math.degrees(result) * 10 / 9
                elif function_name == "acos":
                    result = math.acos(value)
                    # Conversion inverse pour l'affichage
                    if self.angle_unit == "DEG":
                        result = math.degrees(result)
                    elif self.angle_unit == "GRAD":
                        result = math.degrees(result) * 10 / 9
                elif function_name == "atan":
                    result = math.atan(value)
                    # Conversion inverse pour l'affichage
                    if self.angle_unit == "DEG":
                        result = math.degrees(result)
                    elif self.angle_unit == "GRAD":
                        result = math.degrees(result) * 10 / 9

                self.view.set_display_text(str(result))

            elif function_name == "log":
                # Logarithme décimal
                result = math.log10(float(current))
                self.view.set_display_text(str(result))

            elif function_name == "ln":
                # Logarithme népérien
                result = math.log(float(current))
                self.view.set_display_text(str(result))

            elif function_name == "exp":
                # Exponentielle
                result = math.exp(float(current))
                self.view.set_display_text(str(result))

            elif function_name == "x²":
                # Carré
                result = float(current) ** 2
                self.view.set_display_text(str(result))

            elif function_name == "√":
                # Racine carrée
                result = math.sqrt(float(current))
                self.view.set_display_text(str(result))

            elif function_name == "x^y":
                # Puissance (nécessite une deuxième entrée)
                self.view.append_to_display("^")

            elif function_name == "π":
                # Constante pi
                self.view.set_display_text(str(math.pi))

            elif function_name == "e":
                # Constante e
                self.view.set_display_text(str(math.e))

            elif function_name == "x!":
                # Factorielle
                n = int(float(current))
                if n < 0:
                    raise ValueError(
                        "Factorielle non définie pour les nombres négatifs"
                    )
                result = math.factorial(n)
                self.view.set_display_text(str(result))

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
