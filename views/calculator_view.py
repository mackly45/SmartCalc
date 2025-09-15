from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
    QGridLayout,
    QFrame,
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QRectF
from PyQt6.QtGui import (
    QFont,
    QPixmap,
    QColor,
    QPainter,
    QPainterPath,
    QIcon,
    QResizeEvent,
)


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.text = text
        self.icon = None

        # Charger l'image du personnage si c'est un chiffre ou un point
        if text.isdigit() or text in [".", "+", "-", "×", "÷", "=", "%", "C", "±"]:
            try:
                # Mapper les caractères spéciaux aux noms de fichiers
                char_map = {
                    ".": "point",
                    "×": "x",
                    "÷": "div",
                    "=": "equal",
                    "%": "percent",
                    "C": "clear",
                    "±": "plusminus",
                }
                file_text = char_map.get(text, text)

                # Essayer d'abord avec .png, puis avec .jpg
                try:
                    self.icon = QPixmap(f"assets/images/characters/{file_text}.png")
                    if self.icon.isNull():
                        raise FileNotFoundError
                except:
                    self.icon = QPixmap(f"assets/images/characters/{file_text}.jpg")
                    if self.icon.isNull():
                        raise FileNotFoundError
            except Exception as e:
                print(f"Image non trouvée pour le caractère: {text}")
                self.icon = None

        self.update_style()

    def update_style(self, size=60):
        # Ajuster la taille de la police en fonction de la taille du bouton
        font_size = max(18, int(size * 0.3))
        radius = size // 2  # Calcul du rayon pour les coins arrondis

        style = f"""
            QPushButton {{
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: {radius}px;
                font-size: {font_size}px;
                font-weight: bold;
                min-width: {size}px;
                min-height: {size}px;
                max-width: {size}px;
                max-height: {size}px;
            }}
            QPushButton:hover {{
                background-color: #45475a;
            }}
            QPushButton:pressed {{
                background-color: #585b70;
            }}
        """

        self.setStyleSheet(style)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.update_style(size)
        super().resizeEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dessiner l'icône si elle existe
        if hasattr(self, "icon") and self.icon and not self.icon.isNull():
            try:
                # Taille de l'icône (80% de la taille du bouton)
                icon_size = int(min(self.width(), self.height()) * 0.8)
                x = int((self.width() - icon_size) / 2)
                y = int((self.height() - icon_size) / 2)

                # Créer une copie de l'icône avec opacité réduite
                transparent_icon = self.icon.copy()

                # Appliquer une opacité de 40%
                painter.setOpacity(0.4)

                # Dessiner l'icône avec opacité réduite
                scaled_icon = transparent_icon.scaled(
                    icon_size,
                    icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                painter.drawPixmap(x, y, scaled_icon)

                # Réinitialiser l'opacité pour le texte
                painter.setOpacity(1.0)

            except Exception as e:
                print(f"Erreur lors du dessin de l'icône: {e}")

        # Configuration de la police pour le texte
        font = self.font()
        font_size = int(self.height() * 0.4)
        font.setPointSize(font_size)
        font.setBold(True)
        painter.setFont(font)

        # Configuration du texte
        text = self.text
        text_rect = self.rect()

        # Définir les couleurs en fonction du type de bouton
        if text.isdigit():
            text_color = QColor("#f9e2af")  # Jaune pour les chiffres
        elif text in ["+", "-", "×", "÷", "="]:
            text_color = QColor("#f38ba8")  # Rouge pour les opérations
        elif text == "C":
            text_color = QColor("#f38ba8")  # Rouge pour effacer
        elif text == "±":
            text_color = QColor("#a6e3a1")  # Vert pour le changement de signe
        elif text == "%":
            text_color = QColor("#89b4fa")  # Bleu pour le pourcentage
        else:
            text_color = QColor("#cdd6f4")  # Couleur par défaut

        # Ajustement spécial pour le bouton 0
        if text == "0":
            text_rect = text_rect.adjusted(25, 0, 0, 0)
            alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        else:
            alignment = Qt.AlignmentFlag.AlignCenter

        # Dessiner le contour du texte (noir)
        painter.setPen(QColor("#000000"))
        for dx, dy in [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
            offset_rect = text_rect.translated(dx * 2, dy * 2)
            painter.drawText(offset_rect, alignment, text)

        # Dessiner le texte principal avec la couleur appropriée
        painter.setPen(text_color)
        painter.drawText(text_rect, alignment, text)


class CalculatorView(QMainWindow):
    button_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartCalc")
        self.setMinimumSize(300, 500)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
            }
        """
        )

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        # Affichage de l'expression
        self.expression_display = QLabel("")
        self.expression_display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        self.expression_display.setStyleSheet(
            """
            QLabel {
                color: #a6adc8;
                font-size: 18px;
                min-height: 24px;
            }
        """
        )

        # Affichage principal
        self.display = QLabel("0")
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        self.display.setStyleSheet(
            """
            QLabel {
                color: #cdd6f4;
                font-size: 48px;
                font-weight: 300;
                min-height: 60px;
                max-height: 100px;
            }
        """
        )

        # Grille des boutons
        self.buttons_grid = QGridLayout()
        self.buttons_grid.setSpacing(10)

        # Définition des boutons
        buttons = [
            ("C", 0, 0, 1, 1, "background-color: #f38ba8; color: #1e1e2e;"),
            ("±", 0, 1, 1, 1, "background-color: #313244;"),
            ("%", 0, 2, 1, 1, "background-color: #313244;"),
            ("÷", 0, 3, 1, 1, "background-color: #f9e2af; color: #1e1e2e;"),
            ("7", 1, 0, 1, 1, None),
            ("8", 1, 1, 1, 1, None),
            ("9", 1, 2, 1, 1, None),
            ("×", 1, 3, 1, 1, "background-color: #f9e2af; color: #1e1e2e;"),
            ("4", 2, 0, 1, 1, None),
            ("5", 2, 1, 1, 1, None),
            ("6", 2, 2, 1, 1, None),
            ("-", 2, 3, 1, 1, "background-color: #f9e2af; color: #1e1e2e;"),
            ("1", 3, 0, 1, 1, None),
            ("2", 3, 1, 1, 1, None),
            ("3", 3, 2, 1, 1, None),
            ("+", 3, 3, 1, 1, "background-color: #f9e2af; color: #1e1e2e;"),
            ("0", 4, 0, 1, 2, "text-align: left; padding-left: 25px;"),
            (".", 4, 2, 1, 1, None),
            ("=", 4, 3, 1, 1, "background-color: #a6e3a1; color: #1e1e2e;"),
        ]

        # Création des boutons
        self.buttons = {}
        for btn_text, row, col, row_span, col_span, style in buttons:
            btn = ModernButton(btn_text)
            if style:
                btn.setStyleSheet(btn.styleSheet() + style)

            if btn_text == "0":
                btn.setStyleSheet(
                    btn.styleSheet() + "text-align: left; padding-left: 25px;"
                )

            self.buttons_grid.addWidget(btn, row, col, row_span, col_span)
            self.buttons[btn_text] = btn
            btn.clicked.connect(
                lambda checked, text=btn_text: self.on_button_click(text)
            )

        # Ajout des widgets au layout principal
        self.main_layout.addWidget(self.expression_display)
        self.main_layout.addWidget(self.display)
        self.main_layout.addLayout(self.buttons_grid)

    def resizeEvent(self, event):
        # Ajuster la taille de la police en fonction de la taille de la fenêtre
        font_size = max(24, min(self.width(), self.height()) // 15)
        self.display.setStyleSheet(
            f"""
            QLabel {{
                color: #cdd6f4;
                font-size: {font_size}px;
                font-weight: 300;
                min-height: {font_size * 1.5}px;
                max-height: {font_size * 2}px;
            }}
        """
        )
        super().resizeEvent(event)

    def on_button_click(self, text):
        self.button_clicked.emit(text)

    def update_display(self, value):
        self.display.setText(value)

    def update_expression(self, expression):
        self.expression_display.setText(expression)

    def clear_display(self):
        self.display.setText("0")
        self.expression_display.setText("")

    def show_error(self):
        self.display.setText("Error")
        self.expression_display.setText("")
