#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QStatusBar,
    QLabel,
    QTabWidget,
)
from PyQt6.QtCore import Qt, QTimer

from views.calculator_view import CalculatorView
from views.scientific_view import ScientificView
from views.advanced_view import AdvancedView
from views.conversion_view import ConversionView
from views.currency_view import CurrencyView

from models.calculator_model import CalculatorModel
from models.scientific_model import ScientificModel
from models.advanced_model import AdvancedCalculatorModel
from models.conversion_model import ConversionModel
from models.currency_model import CurrencyModel

from controllers.calculator_controller import CalculatorController
from controllers.scientific_controller import ScientificController
from controllers.advanced_controller import AdvancedController
from controllers.conversion_controller import ConversionController
from controllers.currency_controller import CurrencyController


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartCalc - Calculatrice Scientifique")
        self.setMinimumSize(1000, 800)

        # Création des modèles
        self.calculator_model = CalculatorModel()
        self.scientific_model = ScientificModel()
        self.advanced_model = AdvancedCalculatorModel()
        self.conversion_model = ConversionModel()
        self.currency_model = CurrencyModel()

        # Création des vues
        self.calculator_view = CalculatorView()
        self.scientific_view = ScientificView()
        self.advanced_view = AdvancedView()
        self.conversion_view = ConversionView()
        self.currency_view = CurrencyView()

        # Configuration de l'interface
        self.setup_ui()

        # Création des contrôleurs
        self.calculator_controller = CalculatorController(
            self.calculator_model, self.calculator_view
        )
        self.scientific_controller = ScientificController(
            self.scientific_model, self.scientific_view
        )
        self.advanced_controller = AdvancedController(
            self.advanced_model, self.advanced_view
        )
        self.conversion_controller = ConversionController(
            self.conversion_model, self.conversion_view
        )
        self.currency_controller = CurrencyController(
            self.currency_model, self.currency_view
        )

        # Connexion des signaux
        self.setup_connections()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Créer le widget d'onglets
        self.tab_widget = QTabWidget()

        # Ajout des vues à l'interface
        self.tab_widget.addTab(self.calculator_view, "Calculatrice")
        self.tab_widget.addTab(self.scientific_view, "Scientifique")
        self.tab_widget.addTab(self.advanced_view, "Avancé")
        self.tab_widget.addTab(self.conversion_view, "Convertisseur")
        self.tab_widget.addTab(self.currency_view, "Devises")

        # Ajout du widget d'onglets au layout principal
        layout.addWidget(self.tab_widget)

        # Barre d'état
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")

    def setup_connections(self):
        """Établit les connexions entre les signaux et les slots."""
        # Connexion des signaux pour le convertisseur
        self.conversion_view.convert_requested.connect(
            lambda v, f, t, ct: self.conversion_controller.convert_units(v, f, t, ct)
        )
        self.conversion_view.swap_units_requested.connect(
            self.conversion_controller.swap_units
        )
        self.conversion_view.conversion_type_changed.connect(
            self.conversion_controller.set_conversion_type
        )

        # Signaux du contrôleur de conversion
        self.conversion_controller.conversion_result.connect(
            lambda v, u: self.conversion_view.set_result(v)
        )
        self.conversion_controller.error_occurred.connect(
            self.conversion_view.show_error
        )

        # Gestion du changement d'onglet
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """Appelé lors du changement d'onglet"""
        current_tab = self.tab_widget.currentWidget()

        # Initialisation spécifique à chaque onglet
        if current_tab == self.calculator_view:
            self.calculator_controller.initialize_ui()
        elif current_tab == self.scientific_view:
            self.scientific_controller.initialize_ui()
        elif current_tab == self.currency_view:
            self.currency_controller.initialize_ui()
        elif current_tab == self.advanced_view:
            self.advanced_controller.initialize_ui()
        elif current_tab == self.conversion_view:
            # Initialisation spécifique au convertisseur (sans get_conversion_types)
            categories = self.conversion_model.get_categories()
            self.conversion_view.set_categories(categories)
            if categories:
                self.conversion_controller.on_category_changed(categories[0])

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        # Sauvegarde des données si nécessaire
        if hasattr(self, "currency_controller"):
            self.currency_controller.save_data()

        # Nettoyage des contrôleurs
        if hasattr(self, "calculator_controller"):
            self.calculator_controller.cleanup()

        if hasattr(self, "scientific_controller"):
            self.scientific_controller.cleanup()

        if hasattr(self, "advanced_controller"):
            self.advanced_controller.cleanup()

        if hasattr(self, "conversion_controller"):
            self.conversion_controller.cleanup()

        # Fermeture propre de l'application
        event.accept()


# --- Fonctions et classes globales ---


def show_main_app(loading_screen, main_window):
    """Affiche l'application principale après le chargement"""
    main_window.showMaximized()
    loading_screen.close()


class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("SmartCalc - Chargement...")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(400, 400)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Logo
        self.logo_label = QLabel()
        try:
            from PyQt6.QtGui import QPixmap

            pixmap = QPixmap("assets/images/logo.png")
            if not pixmap.isNull():
                self.logo_label.setPixmap(
                    pixmap.scaled(
                        200,
                        200,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")

        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titre
        self.title_label = QLabel("SmartCalc")
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: #cdd6f4;
                font-size: 32px;
                font-weight: bold;
                margin: 20px 0;
            }
        """
        )
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Texte de chargement
        self.loading_label = QLabel("Chargement...")
        self.loading_label.setStyleSheet(
            """
            QLabel {
                color: #a6adc8;
                font-size: 16px;
            }
        """
        )
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajout des widgets au layout
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.loading_label)

        # Centrer la fenêtre
        self.center_window()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        from PyQt6.QtWidgets import QApplication

        screen = QApplication.primaryScreen()
        if screen is not None:
            geo = screen.geometry()
            x = (geo.width() - self.width()) // 2
            y = (geo.height() - self.height()) // 2
            self.move(x, y)


def main():
    """Point d'entrée principal de l'application."""
    app = QApplication(sys.argv)

    # Appliquer un style sombre
    app.setStyle("Fusion")
    app.setStyleSheet(
        """
        QMainWindow, QDialog, QWidget {
            background-color: #1e1e2e;
            color: #cdd6f4;
        }
        QPushButton {
            background-color: #313244;
            color: #cdd6f4;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45475a;
        }
        QPushButton:pressed {
            background-color: #585b70;
        }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            background-color: #1e1e2e;
            color: #cdd6f4;
            border: 1px solid #45475a;
            padding: 5px;
            border-radius: 4px;
        }
        QLabel {
            color: #cdd6f4;
        }
    """
    )

    # Afficher l'écran de chargement
    loading_screen = LoadingScreen()
    loading_screen.show()
    app.processEvents()

    # Créer la fenêtre principale
    main_window = MainWindow()

    # Simuler un temps de chargement
    QTimer.singleShot(2000, lambda: show_main_app(loading_screen, main_window))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
