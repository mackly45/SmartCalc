import math
from typing import Optional, Tuple, Dict, List, Union

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTabWidget,
    QGroupBox,
    QFormLayout,
    QTextEdit,
    QSplitter,
    QSizePolicy,
    QCheckBox,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPen, QPainter, QPixmap

# Import matplotlib avec configuration pour Qt6
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from sympy import symbols, sympify, diff, integrate, solve, limit, oo, series


class AdvancedView(QWidget):
    """
    Vue pour les fonctionnalités avancées de la calculatrice.
    Inclut des outils pour le calcul symbolique, les graphes, etc.
    """

    # Signaux
    calculate_clicked = pyqtSignal(str, dict)  # expression, variables
    plot_clicked = pyqtSignal(str, tuple, tuple)  # expr, x_range, y_range
    solve_clicked = pyqtSignal(str, str)  # equation, variable
    differentiate_clicked = pyqtSignal(str, str, int)  # expr, var, order
    integrate_clicked = pyqtSignal(str, str, float, float)  # expr, var, a, b
    limit_clicked = pyqtSignal(str, str, str, str)  # expr, var, point, direction
    series_clicked = pyqtSignal(str, str, float, int)  # expr, var, point, order

    def __init__(self, parent=None):
        super().__init__(parent)
        self.variables = {}
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        main_layout = QVBoxLayout(self)

        # Création des onglets
        self.tabs = QTabWidget()

        # Onglet Calcul symbolique
        self.symbolic_tab = QWidget()
        self.setup_symbolic_tab()

        # Onglet Graphiques
        self.plot_tab = QWidget()
        self.setup_plot_tab()

        # Onglet Calcul différentiel
        self.calculus_tab = QWidget()
        self.setup_calculus_tab()

        # Ajout des onglets
        self.tabs.addTab(self.symbolic_tab, "Calcul symbolique")
        self.tabs.addTab(self.plot_tab, "Graphiques")
        self.tabs.addTab(self.calculus_tab, "Calcul différentiel")

        # Bouton de retour
        self.back_button = QPushButton("Retour à la calculatrice scientifique")
        self.back_button.clicked.connect(self.go_back)

        # Ajout des composants au layout principal
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.back_button)

    def setup_symbolic_tab(self):
        """Configure l'onglet de calcul symbolique."""
        layout = QVBoxLayout()

        # Zone de saisie de l'expression
        self.expression_input = QLineEdit()
        self.expression_input.setPlaceholderText(
            "Entrez une expression (ex: x**2 + 2*x + 1)"
        )

        # Bouton de calcul
        self.calculate_button = QPushButton("Calculer")
        self.calculate_button.clicked.connect(self.on_calculate_clicked)

        # Zone de résultat
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)

        # Ajout des composants au layout
        layout.addWidget(QLabel("Expression:"))
        layout.addWidget(self.expression_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(QLabel("Résultat:"))
        layout.addWidget(self.result_display)

        self.symbolic_tab.setLayout(layout)

    def setup_plot_tab(self):
        """Configure l'onglet de tracé de courbes."""
        layout = QVBoxLayout()

        # Zone de saisie de la fonction
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("f(x) = ")

        # Paramètres du graphe
        params_layout = QHBoxLayout()

        # Min X
        self.min_x = QLineEdit("-10")
        params_layout.addWidget(QLabel("X min:"))
        params_layout.addWidget(self.min_x)

        # Max X
        self.max_x = QLineEdit("10")
        params_layout.addWidget(QLabel("X max:"))
        params_layout.addWidget(self.max_x)

        # Bouton de tracé
        self.plot_button = QPushButton("Tracer")
        self.plot_button.clicked.connect(self.on_plot_clicked)

        # Zone d'affichage du graphe
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Ajout des composants au layout
        layout.addWidget(QLabel("Fonction à tracer:"))
        layout.addWidget(self.function_input)
        layout.addLayout(params_layout)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.canvas)

        self.plot_tab.setLayout(layout)

    def setup_calculus_tab(self):
        """Configure l'onglet de calcul différentiel."""
        tabs = QTabWidget()

        # Sous-onglet Dérivée
        self.derivative_tab = QWidget()
        self.setup_derivative_tab()

        # Sous-onglet Intégrale
        self.integral_tab = QWidget()
        self.setup_integral_tab()

        # Sous-onglet Limite
        self.limit_tab = QWidget()
        self.setup_limit_tab()

        # Sous-onglet Série
        self.series_tab = QWidget()
        self.setup_series_tab()

        # Ajout des sous-onglets
        tabs.addTab(self.derivative_tab, "Dérivée")
        tabs.addTab(self.integral_tab, "Intégrale")
        tabs.addTab(self.limit_tab, "Limite")
        tabs.addTab(self.series_tab, "Série")

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.calculus_tab.setLayout(layout)

    def setup_derivative_tab(self):
        """Configure le sous-onglet de calcul de dérivée."""
        layout = QVBoxLayout()

        # Expression
        self.deriv_expression = QLineEdit()
        self.deriv_expression.setPlaceholderText("Entrez une expression (ex: x**2)")

        # Variable
        self.deriv_var = QLineEdit("x")

        # Ordre de dérivation
        self.deriv_order = QLineEdit("1")

        # Bouton de calcul
        self.deriv_button = QPushButton("Calculer la dérivée")
        self.deriv_button.clicked.connect(self.on_derivative_clicked)

        # Résultat
        self.deriv_result = QTextEdit()
        self.deriv_result.setReadOnly(True)

        # Formulaire de paramètres
        form = QFormLayout()
        form.addRow("Expression:", self.deriv_expression)
        form.addRow("Variable:", self.deriv_var)
        form.addRow("Ordre:", self.deriv_order)

        # Ajout des composants au layout
        layout.addLayout(form)
        layout.addWidget(self.deriv_button)
        layout.addWidget(QLabel("Résultat:"))
        layout.addWidget(self.deriv_result)

        self.derivative_tab.setLayout(layout)

    def setup_integral_tab(self):
        """Configure le sous-onglet de calcul d'intégrale."""
        layout = QVBoxLayout()

        # Expression
        self.integral_expression = QLineEdit()
        self.integral_expression.setPlaceholderText("Entrez une expression (ex: x**2)")

        # Variable
        self.integral_var = QLineEdit("x")

        # Bornes
        self.lower_bound = QLineEdit("0")
        self.upper_bound = QLineEdit("1")

        # Case à cocher pour l'intégrale indéfinie
        self.indefinite_integral = QCheckBox("Intégrale indéfinie")
        self.indefinite_integral.stateChanged.connect(self.toggle_definite_integral)

        # Bouton de calcul
        self.integral_button = QPushButton("Calculer l'intégrale")
        self.integral_button.clicked.connect(self.on_integral_clicked)

        # Résultat
        self.integral_result = QTextEdit()
        self.integral_result.setReadOnly(True)

        # Formulaire de paramètres
        form = QFormLayout()
        form.addRow("Expression:", self.integral_expression)
        form.addRow("Variable:", self.integral_var)
        form.addRow("Borne inférieure:", self.lower_bound)
        form.addRow("Borne supérieure:", self.upper_bound)

        # Ajout des composants au layout
        layout.addLayout(form)
        layout.addWidget(self.indefinite_integral)
        layout.addWidget(self.integral_button)
        layout.addWidget(QLabel("Résultat:"))
        layout.addWidget(self.integral_result)

        self.integral_tab.setLayout(layout)

    def setup_limit_tab(self):
        """Configure le sous-onglet de calcul de limite."""
        layout = QVBoxLayout()

        # Expression
        self.limit_expression = QLineEdit()
        self.limit_expression.setPlaceholderText("Entrez une expression (ex: sin(x)/x)")

        # Variable et point
        self.limit_var = QLineEdit("x")
        self.limit_point = QLineEdit("0")

        # Direction
        self.limit_direction = QComboBox()
        self.limit_direction.addItems(["+", "-"])

        # Bouton de calcul
        self.limit_button = QPushButton("Calculer la limite")
        self.limit_button.clicked.connect(self.on_limit_clicked)

        # Résultat
        self.limit_result = QTextEdit()
        self.limit_result.setReadOnly(True)

        # Formulaire de paramètres
        form = QFormLayout()
        form.addRow("Expression:", self.limit_expression)
        form.addRow("Variable:", self.limit_var)
        form.addRow("Point:", self.limit_point)
        form.addRow("Direction:", self.limit_direction)

        # Ajout des composants au layout
        layout.addLayout(form)
        layout.addWidget(self.limit_button)
        layout.addWidget(QLabel("Résultat:"))
        layout.addWidget(self.limit_result)

        self.limit_tab.setLayout(layout)

    def setup_series_tab(self):
        """Configure le sous-onglet de développement en série."""
        layout = QVBoxLayout()

        # Expression
        self.series_expression = QLineEdit()
        self.series_expression.setPlaceholderText("Entrez une expression (ex: exp(x))")

        # Variable et point
        self.series_var = QLineEdit("x")
        self.series_point = QLineEdit("0")

        # Ordre
        self.series_order = QLineEdit("5")

        # Bouton de calcul
        self.series_button = QPushButton("Développer en série")
        self.series_button.clicked.connect(self.on_series_clicked)

        # Résultat
        self.series_result = QTextEdit()
        self.series_result.setReadOnly(True)

        # Formulaire de paramètres
        form = QFormLayout()
        form.addRow("Expression:", self.series_expression)
        form.addRow("Variable:", self.series_var)
        form.addRow("Point:", self.series_point)
        form.addRow("Ordre:", self.series_order)

        # Ajout des composants au layout
        layout.addLayout(form)
        layout.addWidget(self.series_button)
        layout.addWidget(QLabel("Développement en série:"))
        layout.addWidget(self.series_result)

        self.series_tab.setLayout(layout)

    def toggle_definite_integral(self, state):
        """Active/désactive les champs de bornes pour l'intégrale."""
        self.lower_bound.setEnabled(not bool(state))
        self.upper_bound.setEnabled(not bool(state))

    def on_calculate_clicked(self):
        """Gère le clic sur le bouton de calcul."""
        expression = self.expression_input.text().strip()
        if expression:
            self.calculate_clicked.emit(expression, self.variables)

    def on_plot_clicked(self):
        """Gère le clic sur le bouton de tracé."""
        expression = self.function_input.text().strip()
        if not expression:
            return

        try:
            x_min = float(self.min_x.text())
            x_max = float(self.max_x.text())

            if x_min >= x_max:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La valeur minimale doit être inférieure à la valeur maximale",
                )
                return

            self.plot_clicked.emit(
                expression,
                (x_min, x_max),
                (None, None),  # y_range sera déterminé automatiquement
            )

        except ValueError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez entrer des valeurs numériques valides pour les bornes",
            )

    def on_derivative_clicked(self):
        """Gère le clic sur le bouton de calcul de dérivée."""
        expression = self.deriv_expression.text().strip()
        variable = self.deriv_var.text().strip()

        if not expression or not variable:
            return

        try:
            order = int(self.deriv_order.text())
            if order < 1:
                raise ValueError("L'ordre doit être un entier positif")

            self.differentiate_clicked.emit(expression, variable, order)

        except ValueError as e:
            QMessageBox.warning(
                self, "Erreur", f"Ordre de dérivation invalide: {str(e)}"
            )

    def on_integral_clicked(self):
        """Gère le clic sur le bouton de calcul d'intégrale."""
        expression = self.integral_expression.text().strip()
        variable = self.integral_var.text().strip()

        if not expression or not variable:
            return

        if self.indefinite_integral.isChecked():
            # Intégrale indéfinie
            self.integrate_clicked.emit(expression, variable, None, None)
        else:
            # Intégrale définie
            try:
                a = float(self.lower_bound.text())
                b = float(self.upper_bound.text())
                self.integrate_clicked.emit(expression, variable, a, b)

            except ValueError:
                QMessageBox.warning(
                    self, "Erreur", "Veuillez entrer des bornes numériques valides"
                )

    def on_limit_clicked(self):
        """Gère le clic sur le bouton de calcul de limite."""
        expression = self.limit_expression.text().strip()
        variable = self.limit_var.text().strip()
        point = self.limit_point.text().strip()

        if not expression or not variable or not point:
            return

        direction = self.limit_direction.currentText()
        self.limit_clicked.emit(expression, variable, point, direction)

    def on_series_clicked(self):
        """Gère le clic sur le bouton de développement en série."""
        expression = self.series_expression.text().strip()
        variable = self.series_var.text().strip()
        point = self.series_point.text().strip()

        if not expression or not variable or not point:
            return

        try:
            point_val = float(point)
            order = int(self.series_order.text())

            if order < 1:
                raise ValueError("L'ordre doit être un entier positif")

            self.series_clicked.emit(expression, variable, point_val, order)

        except ValueError as e:
            QMessageBox.warning(self, "Erreur", f"Valeurs invalides: {str(e)}")

    def show_result(self, result: str):
        """Affiche le résultat du calcul."""
        self.result_display.setText(result)

    def show_derivative_result(self, result: str):
        """Affiche le résultat de la dérivation."""
        self.deriv_result.setText(result)

    def show_integral_result(self, result: str):
        """Affiche le résultat de l'intégration."""
        self.integral_result.setText(result)

    def show_limit_result(self, result: str):
        """Affiche le résultat du calcul de limite."""
        self.limit_result.setText(result)

    def show_series_result(self, result: str):
        """Affiche le résultat du développement en série."""
        self.series_result.setText(result)

    def plot_function(self, x: list, y: list, expression: str):
        """Trace la fonction sur le canevas."""
        # Effacer la figure précédente
        self.figure.clear()

        # Créer un nouvel axe
        ax = self.figure.add_subplot(111)

        # Tracer la fonction
        ax.plot(x, y, "b-", linewidth=2)

        # Ajouter des étiquettes et un titre
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Graphe de {expression}")

        # Activer la grille
        ax.grid(True)

        # Redessiner le canevas
        self.canvas.draw()

    def show_error(self, message: str):
        """Affiche un message d'erreur."""
        QMessageBox.critical(self, "Erreur", message)

    def go_back(self):
        """Retourne à la vue précédente."""
        self.hide()
        if hasattr(self, "parent") and self.parent():
            self.parent().show()
