import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QStackedWidget, QHBoxLayout, QPushButton)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer, QSize

# Import des vues
from views.calculator_view import CalculatorView
from views.currency_view import CurrencyView

# Import des modèles
from models.calculator_model import CalculatorModel
from models.currency_model import CurrencyModel

# Import des contrôleurs
from controllers.calculator_controller import CalculatorController
from controllers.currency_controller import CurrencyController

class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.setWindowTitle("SmartCalc - Chargement...")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
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
            pixmap = QPixmap("assets/images/logo.png")
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(
                    200, 200, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")
        
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Titre
        self.title_label = QLabel("SmartCalc")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #cdd6f4;
                font-size: 32px;
                font-weight: bold;
                margin: 20px 0;
            }
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Texte de chargement
        self.loading_label = QLabel("Chargement...")
        self.loading_label.setStyleSheet("""
            QLabel {
                color: #a6adc8;
                font-size: 16px;
            }
        """)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Ajout des widgets au layout
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.loading_label)
        
        # Centrer la fenêtre
        self.center_window()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("SmartCalc")
        self.setMinimumSize(800, 600)
        
        # Création du widget empilé pour gérer les différentes vues
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Création de la barre de navigation
        self.setup_navbar()
        
        # Initialisation des vues
        self.setup_views()
        
        # Afficher la vue par défaut
        self.show_calculator()
    
    def setup_navbar(self):
        """Configure la barre de navigation"""
        navbar = self.menuBar()
        navbar.setStyleSheet("""
            QMenuBar {
                background-color: #1e1e2e;
                color: #cdd6f4;
                padding: 5px;
                border: none;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #45475a;
            }
            QMenuBar::item:pressed {
                background: #585b70;
            }
        """)
        
        # Menu principal
        menu = navbar.addMenu("☰")
        
        # Actions du menu
        calculator_action = menu.addAction("Calculatrice")
        currency_action = menu.addAction("Convertisseur de devises")
        
        # Connexion des actions
        calculator_action.triggered.connect(self.show_calculator)
        currency_action.triggered.connect(self.show_currency_converter)
    
    def setup_views(self):
        """Initialise toutes les vues de l'application"""
        # Vue de la calculatrice
        self.calculator_model = CalculatorModel()
        self.calculator_view = CalculatorView()
        self.calculator_controller = CalculatorController(
            self.calculator_model, 
            self.calculator_view
        )
        
        # Vue du convertisseur de devises
        self.currency_model = CurrencyModel()
        self.currency_view = CurrencyView()
        self.currency_controller = CurrencyController(
            self.currency_model,
            self.currency_view
        )
        
        # Ajout des vues au widget empilé
        self.stacked_widget.addWidget(self.calculator_view)
        self.stacked_widget.addWidget(self.currency_view)
    
    def show_calculator(self):
        """Affiche la vue de la calculatrice"""
        self.setWindowTitle("SmartCalc - Calculatrice")
        self.stacked_widget.setCurrentIndex(0)
    
    def show_currency_converter(self):
        """Affiche le convertisseur de devises"""
        self.setWindowTitle("SmartCalc - Convertisseur de devises")
        self.stacked_widget.setCurrentIndex(1)
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        # Nettoyage des contrôleurs
        if hasattr(self, 'currency_controller'):
            self.currency_controller.cleanup()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Appliquer un style sombre à toute l'application
    app.setStyle('Fusion')
    app.setStyleSheet("""
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
    """)
    
    # Afficher l'écran de chargement
    loading_screen = LoadingScreen()
    loading_screen.show()
    
    # Forcer l'affichage de l'écran de chargement
    app.processEvents()
    
    # Créer la fenêtre principale (mais ne pas l'afficher tout de suite)
    main_window = MainWindow()
    
    # Simuler un temps de chargement
    QTimer.singleShot(2000, lambda: [
        loading_screen.close(),
        main_window.showMaximized()
    ])
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
