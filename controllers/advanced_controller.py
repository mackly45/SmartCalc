from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import numpy as np
import sympy as sp


class AdvancedController(QObject):
    """Contrôleur pour la vue avancée (graphiques, matrices, factorisation)"""

    def __init__(self, model, view):
        """
        Initialise le contrôleur

        Args:
            model: Instance de AdvancedCalculatorModel
            view: Instance de AdvancedView
        """
        super().__init__()
        self.model = model
        self.view = view

        # Connecter les signaux du modèle
        self.model.plot_updated.connect(self.on_plot_updated)
        self.model.matrix_operation_completed.connect(
            self.on_matrix_operation_completed
        )
        self.model.factorization_completed.connect(self.on_factorization_completed)
        self.model.error_occurred.connect(self.on_error_occurred)

        # Connecter les signaux de la vue
        self.setup_connections()

    def setup_connections(self):
        """Établit les connexions entre la vue et le contrôleur"""
        # Connexions pour les graphiques
        if hasattr(self.view, "plot_button"):
            self.view.plot_button.clicked.connect(self.on_plot_requested)

        # Connexions pour les matrices
        if hasattr(self.view, "matrix_add_button"):
            self.view.matrix_add_button.clicked.connect(self.on_matrix_add)
        if hasattr(self.view, "matrix_multiply_button"):
            self.view.matrix_multiply_button.clicked.connect(self.on_matrix_multiply)
        if hasattr(self.view, "matrix_determinant_button"):
            self.view.matrix_determinant_button.clicked.connect(
                self.on_matrix_determinant
            )
        if hasattr(self.view, "matrix_inverse_button"):
            self.view.matrix_inverse_button.clicked.connect(self.on_matrix_inverse)

        # Connexions pour la factorisation
        if hasattr(self.view, "factorize_button"):
            self.view.factorize_button.clicked.connect(self.on_factorize_requested)

    # Gestion des événements des graphiques
    @pyqtSlot()
    def on_plot_requested(self):
        """Appelé lorsque l'utilisateur demande un tracé"""
        try:
            expression = self.view.get_expression()
            x_min = self.view.get_x_min()
            x_max = self.view.get_x_max()

            if not expression:
                self.view.show_error("Veuillez entrer une expression")
                return

            self.model.plot_function(expression, x_min, x_max)

        except Exception as e:
            self.view.show_error(f"Erreur lors de la préparation du tracé: {str(e)}")

    @pyqtSlot(np.ndarray, np.ndarray)
    def on_plot_updated(self, x, y):
        """Appelé lorsque le tracé est mis à jour"""
        self.view.update_plot(x, y)
        self.model.add_to_history(
            "Tracé de fonction",
            {
                "expression": self.view.get_expression(),
                "x_min": self.view.get_x_min(),
                "x_max": self.view.get_x_max(),
            },
            f"Tracé de {self.view.get_expression()} sur [{self.view.get_x_min()}, {self.view.get_x_max()}]",
        )

    # Gestion des événements des matrices
    @pyqtSlot()
    def on_matrix_add(self):
        """Gère l'addition de matrices"""
        try:
            matrix_a = self.view.get_matrix_a()
            matrix_b = self.view.get_matrix_b()

            if not matrix_a or not matrix_b:
                self.view.show_error("Les deux matrices doivent être définies")
                return

            self.model.set_matrix_a(matrix_a)
            self.model.set_matrix_b(matrix_b)
            self.model.add_matrices()

        except Exception as e:
            self.view.show_error(f"Erreur lors de l'addition des matrices: {str(e)}")

    @pyqtSlot()
    def on_matrix_multiply(self):
        """Gère la multiplication de matrices"""
        try:
            matrix_a = self.view.get_matrix_a()
            matrix_b = self.view.get_matrix_b()

            if not matrix_a or not matrix_b:
                self.view.show_error("Les deux matrices doivent être définies")
                return

            self.model.set_matrix_a(matrix_a)
            self.model.set_matrix_b(matrix_b)
            self.model.multiply_matrices()

        except Exception as e:
            self.view.show_error(
                f"Erreur lors de la multiplication des matrices: {str(e)}"
            )

    @pyqtSlot()
    def on_matrix_determinant(self):
        """Calcule le déterminant d'une matrice"""
        try:
            matrix = self.view.get_matrix_a()
            if matrix is None:
                matrix = self.view.get_matrix_b()

            if matrix is None:
                self.view.show_error("Aucune matrice définie")
                return

            det = self.model.calculate_determinant(np.array(matrix))
            if det is not None:
                self.view.show_result(f"Déterminant: {det:.4f}")
                self.model.add_to_history(
                    "Calcul du déterminant",
                    {"matrix": matrix},
                    f"Déterminant = {det:.4f}",
                )

        except Exception as e:
            self.view.show_error(f"Erreur lors du calcul du déterminant: {str(e)}")

    @pyqtSlot()
    def on_matrix_inverse(self):
        """Calcule l'inverse d'une matrice"""
        try:
            matrix = self.view.get_matrix_a()
            if matrix is None:
                matrix = self.view.get_matrix_b()

            if matrix is None:
                self.view.show_error("Aucune matrice définie")
                return

            inverse = self.model.calculate_inverse(np.array(matrix))
            if inverse is not None:
                self.view.show_matrix(inverse, "Matrice inverse")
                self.model.add_to_history(
                    "Calcul de l'inverse",
                    {"matrix": matrix},
                    "Matrice inverse calculée",
                )

        except Exception as e:
            self.view.show_error(f"Erreur lors du calcul de l'inverse: {str(e)}")

    @pyqtSlot(np.ndarray)
    def on_matrix_operation_completed(self, result):
        """Appelé lorsqu'une opération sur les matrices est terminée"""
        self.view.show_matrix(result, "Résultat")

    # Gestion des événements de factorisation
    @pyqtSlot()
    def on_factorize_requested(self):
        """Gère la demande de factorisation"""
        try:
            expression = self.view.get_expression_to_factor()
            if not expression:
                self.view.show_error("Veuillez entrer une expression à factoriser")
                return

            result = self.model.factor_expression(expression)
            if result is not None:
                self.view.show_factorization_result(result)
                self.model.add_to_history(
                    "Factorisation", {"expression": expression}, f"Résultat: {result}"
                )

                # Afficher l'analyse de l'expression
                analysis = self.model.analyze_expression(expression)
                if analysis is not None:
                    self.view.show_analysis(analysis)

        except Exception as e:
            self.view.show_error(f"Erreur lors de la factorisation: {str(e)}")

    @pyqtSlot(str)
    def on_factorization_completed(self, result):
        """Appelé lorsque la factorisation est terminée"""
        self.view.show_factorization_result(result)

    # Gestion des erreurs
    @pyqtSlot(str)
    def on_error_occurred(self, error_message):
        """Affiche un message d'erreur"""
        self.view.show_error(error_message)

    # Méthodes utilitaires
    def initialize_ui(self):
        """Initialise l'interface utilisateur avec les données du modèle"""
        # Initialisation de l'interface utilisateur
        pass

    def initialize(self):
        """Initialise le contrôleur (pour compatibilité descendante)"""
        self.initialize_ui()

    def cleanup(self):
        """Nettoie les ressources"""
        # Sauvegarder l'historique si nécessaire
        pass
