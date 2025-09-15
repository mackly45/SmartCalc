from PyQt6.QtCore import QObject, pyqtSignal
import math


class ScientificController(QObject):
    """
    Contrôleur pour la calculatrice scientifique.
    Gère la logique de calcul et la communication entre le modèle et la vue.
    """

    def __init__(self, model, view):
        """
        Initialise le contrôleur avec le modèle et la vue.

        Args:
            model: Instance de ScientificCalculatorModel
            view: Instance de ScientificView
        """
        super().__init__()
        self.model = model
        self.view = view

        # Configuration initiale
        self.setup_connections()
        self.initialize_ui()

    def setup_connections(self):
        """Établit les connexions entre les signaux et les slots"""
        # Connexion des signaux de la vue
        self.view.expression_evaluated.connect(self.evaluate_expression)
        self.view.function_pressed.connect(self.handle_function)
        self.view.memory_operation.connect(self.handle_memory_operation)
        self.view.statistics_operation.connect(self.handle_statistics)

        # Mise à jour du mode d'angle quand il change
        self.view.angle_mode.currentTextChanged.connect(self.update_angle_mode)

    def initialize_ui(self):
        """Initialise l'interface utilisateur avec les données du modèle"""
        # Définir le mode d'angle actuel
        self.view.angle_mode.setCurrentText(self.model.settings["angle_mode"])

        # Initialiser les points de données
        if not hasattr(self.view, "data_points"):
            self.view.data_points = []

        # Mettre à jour l'affichage de la mémoire
        self.view.update_memory_display(self.model.memory)

    def evaluate_expression(self, expression, _=None):
        """
        Évalue une expression mathématique.

        Args:
            expression: L'expression à évaluer
            _: Paramètre inutilisé (pour la compatibilité avec le signal)
        """
        try:
            # Nettoyer l'expression
            expression = expression.strip()
            if not expression:
                self.view.set_result("0")
                return

            # Remplacer les symboles spéciaux
            expr = expression.replace("^", "**").replace("√", "sqrt")

            # Évaluer l'expression
            result = self.model.evaluate_expression(expr)

            # Formater le résultat
            formatted_result = self.model.format_number(result)

            # Mettre à jour la vue
            self.view.set_expression(expression)
            self.view.set_result(formatted_result)

            # Ajouter à l'historique
            self.model.add_to_history(expression, formatted_result)

            # Mettre à jour l'affichage de l'historique si visible
            if hasattr(self.view, "history_visible") and self.view.history_visible:
                self.view.update_history_display()

        except Exception as e:
            print(f"Erreur d'évaluation: {e}")
            self.view.set_result("Erreur")

    def handle_function(self, function_name):
        """
        Gère les appels de fonction spéciaux.

        Args:
            function_name: Nom de la fonction appelée
        """
        try:
            current = self.view.result_display.text()

            if function_name == "x²":
                result = self.model.evaluate_expression(f"({current})**2")
            elif function_name == "x³":
                result = self.model.evaluate_expression(f"({current})**3")
            elif function_name == "1/x":
                result = self.model.evaluate_expression(f"1/({current})")
            elif function_name == "|x|":
                result = abs(float(current))
            elif function_name == "e^x":
                result = math.exp(float(current))
            elif function_name == "10^x":
                result = 10 ** float(current)
            elif function_name == "log":
                result = math.log10(float(current))
            elif function_name == "ln":
                result = math.log(float(current))
            elif function_name == "x!":
                result = math.factorial(int(float(current)))
            elif function_name == "√":
                result = math.sqrt(float(current))
            elif function_name == "³√":
                result = float(current) ** (1 / 3)
            else:
                # Pour les autres fonctions, on les ajoute simplement à l'affichage
                self.view.result_display.setText(f"{function_name}({current})")
                return

            # Mettre à jour l'affichage avec le résultat
            formatted_result = self.model.format_number(result)
            self.view.set_result(formatted_result)

        except (ValueError, OverflowError) as e:
            print(f"Erreur de fonction: {e}")
            self.view.set_result("Erreur")

    def handle_memory_operation(self, operation, value):
        """
        Gère les opérations sur la mémoire.

        Args:
            operation: L'opération à effectuer ('add', 'subtract', 'clear', 'recall')
            value: La valeur à utiliser pour l'opération
        """
        try:
            if operation == "add":
                self.model.memory_add(value)
            elif operation == "subtract":
                self.model.memory_subtract(value)
            elif operation == "clear":
                self.model.memory_clear()
            elif operation == "recall":
                # Récupérer la valeur en mémoire et l'ajouter à l'affichage
                mem_value = self.model.memory_recall()
                current = self.view.result_display.text()
                if current == "0" or current == "Erreur":
                    self.view.result_display.setText(str(mem_value))
                else:
                    self.view.result_display.setText(current + str(mem_value))
                return

            # Mettre à jour l'affichage de la mémoire
            self.view.update_memory_display(self.model.memory)

        except Exception as e:
            print(f"Erreur de mémoire: {e}")
            self.view.set_result("Erreur")

    def handle_statistics(self, operation, data=None):
        """
        Gère les opérations statistiques

        Args:
            operation: L'opération à effectuer ('add', 'clear', 'calculate')
            data: Données à utiliser (pour 'add')

        Returns:
            Résultat de l'opération ou None en cas d'erreur
        """
        try:
            # S'assurer que data_points existe
            if not hasattr(self.view, "data_points"):
                self.view.data_points = []

            if operation == "add" and data is not None:
                # Convertir les données en liste de nombres
                if isinstance(data, str):
                    numbers = [float(x.strip()) for x in data.split(",") if x.strip()]
                    self.view.data_points.extend(numbers)
                elif isinstance(data, (list, tuple)):
                    self.view.data_points.extend(data)
                return True

            elif operation == "clear":
                self.view.data_points = []
                return True

            elif operation == "calculate":
                if not hasattr(self.view, "data_points") or not self.view.data_points:
                    return None

                results = {
                    "count": len(self.view.data_points),
                    "sum": sum(self.view.data_points),
                    "mean": self.model.calculate_mean(self.view.data_points),
                    "median": self.model.calculate_median(self.view.data_points),
                    "mode": self.model.calculate_mode(self.view.data_points),
                    "std_dev": self.model.calculate_std_dev(self.view.data_points),
                    "variance": self.model.calculate_variance(self.view.data_points),
                    "min": min(self.view.data_points),
                    "max": max(self.view.data_points),
                    "range": max(self.view.data_points) - min(self.view.data_points),
                }
                return results

        except Exception as e:
            print(f"Erreur lors du traitement statistique: {e}")
            return None

    def update_angle_mode(self, mode):
        """
        Met à jour le mode d'angle (degrés, radians, grades).

        Args:
            mode: Le nouveau mode d'angle ('DEG', 'RAD' ou 'GRAD')
        """
        if self.model.set_angle_mode(mode):
            # Si le mode a été changé avec succès, on réévalue l'expression actuelle
            current = self.view.result_display.text()
            if current and current != "Erreur":
                self.evaluate_expression(current)

    def update_statistics_display(self):
        """Met à jour l'affichage des statistiques"""
        try:
            # Vérifier que les labels existent
            if not all(
                hasattr(self.view, label)
                for label in [
                    "mean_label",
                    "median_label",
                    "mode_label",
                    "std_dev_label",
                    "variance_label",
                ]
            ):
                return

            # Vérifier que data_points existe et n'est pas vide
            if not hasattr(self.view, "data_points") or not self.view.data_points:
                self.view.mean_label.setText("-")
                self.view.median_label.setText("-")
                self.view.mode_label.setText("-")
                self.view.std_dev_label.setText("-")
                self.view.variance_label.setText("-")
                return

            try:
                # Calculer les statistiques
                mean = self.model.calculate_mean(self.view.data_points)
                median = self.model.calculate_median(self.view.data_points)
                mode = self.model.calculate_mode(self.view.data_points)
                std_dev = self.model.calculate_std_dev(self.view.data_points)
                variance = self.model.calculate_variance(self.view.data_points)

                # Mettre à jour l'interface
                self.view.mean_label.setText(f"{mean:.4f}")
                self.view.median_label.setText(f"{median:.4f}")

                if isinstance(mode, list):
                    self.view.mode_label.setText(", ".join(f"{m:.4f}" for m in mode))
                else:
                    self.view.mode_label.setText(f"{mode:.4f}")

                self.view.std_dev_label.setText(f"{std_dev:.4f}")
                self.view.variance_label.setText(f"{variance:.4f}")

            except Exception as calc_error:
                print(f"Erreur lors du calcul des statistiques: {calc_error}")
                self.view.mean_label.setText("Erreur")
                self.view.median_label.setText("Erreur")
                self.view.mode_label.setText("Erreur")
                self.view.std_dev_label.setText("Erreur")
                self.view.variance_label.setText("Erreur")

        except Exception as e:
            print(f"Erreur inattendue dans update_statistics_display: {e}")

    def cleanup(self):
        """Nettoie les ressources utilisées par le contrôleur"""
        # Nettoyer les connexions de signaux
        try:
            if hasattr(self.view, "expression_evaluated"):
                self.view.expression_evaluated.disconnect()
            if hasattr(self.view, "function_pressed"):
                self.view.function_pressed.disconnect()
            if hasattr(self.view, "memory_operation"):
                self.view.memory_operation.disconnect()
            if hasattr(self.view, "statistics_operation"):
                self.view.statistics_operation.disconnect()
            if hasattr(self.view, "angle_mode") and hasattr(
                self.view.angle_mode, "currentTextChanged"
            ):
                self.view.angle_mode.currentTextChanged.disconnect()
        except Exception as e:
            print(f"Erreur lors du nettoyage des connexions: {e}")

        # Nettoyer les références
        self.model = None
        self.view = None
