from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal


class ConversionView(QWidget):
    """
    Vue pour le convertisseur d'unités.
    Permet de convertir entre différentes unités de mesure.
    """

    # Signaux
    convert_clicked = pyqtSignal(float, str, str)  # valeur, unité_source, unité_cible
    category_changed = pyqtSignal(str)  # catégorie sélectionnée
    back_clicked = pyqtSignal()  # Retour à la calculatrice
    swap_units_requested = pyqtSignal()
    conversion_type_changed = pyqtSignal(str)
    convert_requested = pyqtSignal(float, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        # Configuration de la fenêtre
        self.setWindowTitle("Convertisseur d'unités")
        self.setMinimumSize(400, 300)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Bouton de retour
        self.back_button = QPushButton("← Retour à la calculatrice")
        self.back_button.clicked.connect(self.back_clicked)

        # Groupe pour la sélection de la catégorie
        category_group = QGroupBox("Catégorie de conversion")
        self.category_combo = QComboBox()

        # Les catégories seront ajoutées par le contrôleur
        category_layout = QVBoxLayout()
        category_layout.addWidget(self.category_combo)
        category_group.setLayout(category_layout)

        # Groupe pour les unités et la conversion
        conversion_group = QGroupBox("Conversion")
        form_layout = QGridLayout()

        # Champ de saisie
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Entrez une valeur")
        self.value_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Listes déroulantes pour les unités
        self.from_unit_combo = QComboBox()
        self.to_unit_combo = QComboBox()

        # Bouton d'inversion des unités
        self.swap_button = QPushButton("⇅")
        self.swap_button.setFixedWidth(40)

        # Champ de résultat
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Bouton de conversion
        self.convert_button = QPushButton("Convertir")

        # Ajout des widgets au layout
        form_layout.addWidget(QLabel("Valeur à convertir:"), 0, 0)
        form_layout.addWidget(self.value_input, 0, 1)
        form_layout.addWidget(self.from_unit_combo, 0, 2)

        form_layout.addWidget(QLabel("Résultat:"), 1, 0)
        form_layout.addWidget(self.result_display, 1, 1)
        form_layout.addWidget(self.to_unit_combo, 1, 2)

        form_layout.addWidget(self.swap_button, 0, 3, 2, 1)
        form_layout.addWidget(self.convert_button, 2, 0, 1, 4)

        conversion_group.setLayout(form_layout)

        # Groupe pour le type de conversion
        type_group = QGroupBox("Type de conversion")
        type_layout = QVBoxLayout()
        self.conversion_type_combo = QComboBox()
        type_layout.addWidget(self.conversion_type_combo)
        type_group.setLayout(type_layout)

        # Zone de défilement
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Ajout des groupes au layout principal
        scroll_layout.addWidget(category_group)
        scroll_layout.addWidget(type_group)
        scroll_layout.addWidget(conversion_group)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(self.back_button)
        main_layout.addWidget(scroll)

        # Connexion des signaux
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.convert_button.clicked.connect(self.on_convert_clicked)
        self.swap_button.clicked.connect(self.on_swap_clicked)
        self.conversion_type_combo.currentTextChanged.connect(
            self.on_conversion_type_changed
        )
        self.value_input.returnPressed.connect(self.on_convert_clicked)
        # Label pour l’historique
        self.history_label = QLabel("Aucune conversion récente")
        scroll_layout.addWidget(self.history_label)


    def on_category_changed(self, category):
        """Gère le changement de catégorie."""
        self.category_changed.emit(category)

    def on_convert_clicked(self):
        """Gère le clic sur le bouton de conversion."""
        try:
            value = float(self.value_input.text())
            from_unit = self.from_unit_combo.currentText()
            to_unit = self.to_unit_combo.currentText()
            conv_type = self.conversion_type_combo.currentText()

            if from_unit and to_unit:
                self.convert_requested.emit(value, from_unit, to_unit, conv_type)
        except ValueError:
            self.result_display.setText("Valeur invalide")

    def on_swap_clicked(self):
        """Inverse les unités source et cible."""
        current_from = self.from_unit_combo.currentIndex()
        current_to = self.to_unit_combo.currentIndex()

        self.from_unit_combo.setCurrentIndex(current_to)
        self.to_unit_combo.setCurrentIndex(current_from)

        # Si une conversion a déjà été effectuée, on la relance
        if self.result_display.text() and self.value_input.text():
            self.on_convert_clicked()

        self.swap_units_requested.emit()

    def on_conversion_type_changed(self, conversion_type):
        """Gère le changement de type de conversion."""
        self.conversion_type_changed.emit(conversion_type)

    def set_categories(self, categories):
        """Définit les catégories disponibles."""
        self.category_combo.clear()
        self.category_combo.addItems(categories)

    def set_units(self, units):
        """Définit les unités disponibles pour la catégorie sélectionnée."""
        current_from = self.from_unit_combo.currentText()
        current_to = self.to_unit_combo.currentText()

        self.from_unit_combo.clear()
        self.to_unit_combo.clear()

        if units:
            self.from_unit_combo.addItems(units)
            self.to_unit_combo.addItems(units)

            # Essayer de conserver la sélection précédente si possible
            if current_from in units and current_to in units:
                self.from_unit_combo.setCurrentText(current_from)
                self.to_unit_combo.setCurrentText(current_to)
            else:
                # Par défaut, sélectionner la première et la deuxième unité
                self.from_unit_combo.setCurrentIndex(0)
                if len(units) > 1:
                    self.to_unit_combo.setCurrentIndex(1)

    def set_result(self, result):
        """Affiche le résultat de la conversion."""
        self.result_display.setText(str(result))

    def clear(self):
        """Réinitialise l'interface."""
        self.value_input.clear()
        self.result_display.clear()
        self.from_unit_combo.setCurrentIndex(0)
        if self.to_unit_combo.count() > 1:
            self.to_unit_combo.setCurrentIndex(1)

    def update_conversion_types(self, types):
        """Met à jour la liste des types de conversion disponibles"""
        current = self.conversion_type_combo.currentText()
        self.conversion_type_combo.clear()
        self.conversion_type_combo.addItems(types)
        if current in types:
            self.conversion_type_combo.setCurrentText(current)

    def update_history(self, history):
        """Met à jour l'affichage de l'historique"""
        if not history:
            self.history_label.setText("Aucune conversion récente")
            return

        history_text = []
        for entry in history:
            from_val = f"{entry['from_value']:,.2f}".replace(",", " ").replace(".", ",")
            to_val = f"{entry['to_value']:,.2f}".replace(",", " ").replace(".", ",")
            text = (
                f"{from_val} {entry['from_unit']} → {to_val} {entry['to_unit']} "
                f"({entry['type']})"
            )
            history_text.append(text)

        self.history_label.setText("\n".join(history_text))

    def show_error(self, message):
        """Affiche un message d'erreur"""
        self.result_display.setText(f"Erreur: {message}")
        self.result_display.setStyleSheet("background-color: #ffdddd;")
