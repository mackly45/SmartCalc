import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QSplashScreen, QFrame)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer

class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("SmartCalc - Loading...")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(400, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Add logo
        self.logo_label = QLabel()
        try:
            pixmap = QPixmap("assets/images/logo.png")
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, 
                                                     Qt.TransformationMode.SmoothTransformation))
            else:
                print("Erreur: Impossible de charger le logo. Le fichier est peut-être corrompu.")
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")
            
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add title
        self.title_label = QLabel("SmartCalc")
        self.title_label.setStyleSheet("""
            color: #cdd6f4;
            font-size: 32px;
            font-weight: bold;
            margin: 20px 0;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add loading text
        self.loading_label = QLabel("Chargement...")
        self.loading_label.setStyleSheet("""
            color: #a6adc8;
            font-size: 16px;
        """)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.loading_label)
        
        # Center the window
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()
    
    # Process events to show the loading screen
    app.processEvents()
    
    # Import main components after showing loading screen
    from views.calculator_view import CalculatorView
    from models.calculator_model import CalculatorModel
    from controllers.calculator_controller import CalculatorController
    
    # Create MVC components
    model = CalculatorModel()
    view = CalculatorView()
    controller = CalculatorController(model, view)
    
    # Close loading screen and show main window after delay
    QTimer.singleShot(2000, lambda: [loading_screen.close(), view.show()])
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
