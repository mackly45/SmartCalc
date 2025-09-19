from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QComboBox,
    QGroupBox,
    QLineEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal

# QtGui unused imports removed (QFont, QIcon)


class ScientificView(QWidget):
    """
    Vue pour la calculatrice scientifique.
    Étend les fonctionnalités de base avec des opérations scientifiques.
    """

    # Signaux
    button_clicked = pyqtSignal(str)  # Bouton standard cliqué
    function_clicked = pyqtSignal(str)  # Fonction scientifique cliquée
    angle_unit_changed = pyqtSignal(str)  # Unité d'angle modifiée
    calculate_clicked = pyqtSignal()  # Calcul demandé
    clear_clicked = pyqtSignal()  # Effacer l'affichage
    backspace_clicked = pyqtSignal()  # Effacer le dernier caractère

    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle_unit = "DEG"  # Unité d'angle par défaut: degrés
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        # Configuration de la fenêtre
        self.setWindowTitle("Calculatrice Scientifique")
        self.setMinimumSize(400, 600)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Zone d'affichage
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setMaxLength(30)

        # Taille de police plus grande pour l'affichage
        font = self.display.font()
        font.setPointSize(18)
        self.display.setFont(font)

        # Hauteur fixe pour la zone d'affichage
        self.display.setMinimumHeight(60)
        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        # Sélecteur d'unité d'angle
        self.angle_unit_combo = QComboBox()
        self.angle_unit_combo.addItems(["DEG", "RAD", "GRAD"])
        self.angle_unit_combo.currentTextChanged.connect(self.on_angle_unit_changed)

        # Layout pour l'affichage et le sélecteur d'unité
        display_layout = QHBoxLayout()
        display_layout.addWidget(self.display)
        display_layout.addWidget(self.angle_unit_combo)

        # Groupe pour les boutons de fonctions scientifiques
        sci_functions = QGroupBox("Fonctions")
        sci_layout = QGridLayout()

        # Boutons des fonctions scientifiques
        sci_buttons = [
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("tan", 0, 2),
            ("asin", 1, 0),
            ("acos", 1, 1),
            ("atan", 1, 2),
            ("log", 2, 0),
            ("ln", 2, 1),
            ("exp", 2, 2),
            ("x²", 3, 0),
            ("√", 3, 1),
            ("x^y", 3, 2),
            ("π", 4, 0),
            ("e", 4, 1),
            ("x!", 4, 2),
        ]

        # Création des boutons de fonctions
        for text, row, col in sci_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.on_function_click(t))
            sci_layout.addWidget(btn, row, col, 1, 1)

        sci_functions.setLayout(sci_layout)

        # Groupe pour les boutons numériques et opérations
        calc_group = QGroupBox("Calculatrice")
        calc_layout = QGridLayout()

        # Boutons de la calculatrice
        buttons = [
            ("7", 0, 0),
            ("8", 0, 1),
            ("9", 0, 2),
            ("/", 0, 3),
            ("C", 0, 4),
            ("4", 1, 0),
            ("5", 1, 1),
            ("6", 1, 2),
            ("*", 1, 3),
            ("⌫", 1, 4),
            ("1", 2, 0),
            ("2", 2, 1),
            ("3", 2, 2),
            ("-", 2, 3),
            ("±", 2, 4),
            ("0", 3, 0),
            (".", 3, 1),
            ("%", 3, 2),
            ("+", 3, 3),
            ("=", 3, 4),
            ("(", 4, 0),
            (")", 4, 1),
            ("^", 4, 2),
            ("1/x", 4, 3),
            ("|x|", 4, 4),
        ]

        # Création des boutons
        for text, row, col in buttons:
            btn = QPushButton(text)

            # Style des boutons spéciaux
            if text in ["C", "⌫", "±", "="]:
                btn.setStyleSheet(
                    "QPushButton { background-color: #ff9500; color: white; }"
                    "QPushButton:pressed { background-color: #cc7700; }"
                )

            # Connexion des signaux
            if text == "=":
                btn.clicked.connect(self.calculate_clicked)
            elif text == "C":
                btn.clicked.connect(self.clear_clicked)
            elif text == "⌫":
                btn.clicked.connect(self.backspace_clicked)
            else:
                btn.clicked.connect(lambda checked, t=text: self.button_clicked.emit(t))

            calc_layout.addWidget(btn, row, col, 1, 1)

        calc_group.setLayout(calc_layout)

        # Ajout des widgets au layout principal
        main_layout.addLayout(display_layout)
        main_layout.addWidget(sci_functions)
        main_layout.addWidget(calc_group)

    def on_function_click(self, function_name):
        """Gère le clic sur un bouton de fonction scientifique."""
        self.function_clicked.emit(function_name)

    def on_angle_unit_changed(self, unit):
        """Gère le changement d'unité d'angle."""
        self.angle_unit = unit
        self.angle_unit_changed.emit(unit)

    def get_display_text(self) -> str:
        """Retourne le texte actuellement affiché."""
        return self.display.text()

    def set_display_text(self, text: str):
        """Définit le texte à afficher."""
        self.display.setText(text)

    def append_to_display(self, text: str):
        """Ajoute du texte à l'affichage actuel."""
        self.display.setText(self.display.text() + text)

    def clear_display(self):
        """Efface l'affichage."""
        self.display.clear()

    def backspace(self):
        """Efface le dernier caractère de l'affichage."""
        current_text = self.display.text()
        self.display.setText(current_text[:-1])

    def set_error(self, message: str):
        """Affiche un message d'erreur."""
        self.display.setText(f"Erreur: {message}")

    def toggle_sign(self):
        """Inverse le signe de la valeur affichée."""
        current_text = self.display.text()
        if current_text and current_text[0] == "-":
            self.display.setText(current_text[1:])
        elif current_text:
            self.display.setText("-" + current_text)

    def get_angle_unit(self) -> str:
        """Retourne l'unité d'angle actuelle."""
        return self.angle_unit
