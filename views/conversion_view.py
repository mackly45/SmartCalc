from PyQt6 import QtWidgets as QtW, QtCore as QtC
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QFormLayout,
    QGroupBox,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List, Dict, Any


class ConversionView(QWidget):
    """
    Vue pour l'interface de conversion d'unités.
    Gère l'affichage et les interactions utilisateur.
    """

    # Signaux émis vers le contrôleur
    convert_requested = pyqtSignal(
        float, str, str, str
    )  # value, from_unit, to_unit, conv_type
    swap_units_requested = pyqtSignal()
    conversion_type_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Initialise l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout()

        # Zone de défilement
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Groupe pour la sélection du type de conversion
        type_group = QGroupBox("Type de conversion")
        type_layout = QVBoxLayout()

        self.conversion_type_combo = QComboBox()
        type_layout.addWidget(self.conversion_type_combo)
        type_group.setLayout(type_layout)

        # Groupe pour la conversion
        convert_group = QGroupBox("Conversion")
        convert_layout = QFormLayout()

        # Ligne de saisie et sélection d'unité source
        self.input_value = QLineEdit()
        self.input_value.setPlaceholderText("Entrez une valeur")
        self.input_value.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.from_unit_combo = QComboBox()

        # Bouton pour échanger les unités
        self.swap_button = QPushButton("⇅")
        self.swap_button.setToolTip("Échanger les unités")
        self.swap_button.setMaximumWidth(40)

        # Champ de résultat et sélection d'unité cible
        self.result_value = QLineEdit()
        self.result_value.setReadOnly(True)
        self.result_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_value.setStyleSheet("background-color: #f0f0f0;")

        self.to_unit_combo = QComboBox()

        # Layout pour les champs de saisie et de résultat
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_value)
        input_layout.addWidget(self.from_unit_combo)

        result_layout = QHBoxLayout()
        result_layout.addWidget(self.result_value)
        result_layout.addWidget(self.to_unit_combo)

        # Ajout des champs au formulaire
        convert_layout.addRow("De:", input_layout)
        convert_layout.addRow("", self.swap_button)
        convert_layout.addRow("À:", result_layout)

        # Bouton de conversion
        self.convert_button = QPushButton("Convertir")
        self.convert_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )

        convert_layout.addRow(self.convert_button)
        convert_group.setLayout(convert_layout)

        # Groupe pour l'historique
        history_group = QGroupBox("Historique des conversions")
        history_layout = QVBoxLayout()

        self.history_label = QLabel("Aucune conversion récente")
        self.history_label.setWordWrap(True)
        self.history_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Zone de défilement pour l'historique
        history_scroll = QScrollArea()
        history_scroll.setWidgetResizable(True)
        history_scroll.setWidget(self.history_label)
        history_scroll.setMinimumHeight(100)

        history_layout.addWidget(history_scroll)
        history_group.setLayout(history_layout)

        # Ajout des groupes au layout principal
        scroll_layout.addWidget(type_group)
        scroll_layout.addWidget(convert_group)
        scroll_layout.addWidget(history_group)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def connect_signals(self):
        """Connecte les signaux aux slots"""
        self.convert_button.clicked.connect(self.on_convert_clicked)
        self.swap_button.clicked.connect(self.on_swap_clicked)
        self.conversion_type_combo.currentTextChanged.connect(
            self.on_conversion_type_changed
        )
        self.input_value.returnPressed.connect(self.on_convert_clicked)

    def update_conversion_types(self, types):
        """Met à jour la liste des types de conversion disponibles"""
        current = self.conversion_type_combo.currentText()
        self.conversion_type_combo.clear()
        self.conversion_type_combo.addItems(types)
        if current in types:
            self.conversion_type_combo.setCurrentText(current)

    def update_units(self, units):
        """Met à jour les listes déroulantes des unités"""
        current_from = (
            self.from_unit_combo.currentText()
            if self.from_unit_combo.count() > 0
            else None
        )
        current_to = (
            self.to_unit_combo.currentText() if self.to_unit_combo.count() > 0 else None
        )

        self.from_unit_combo.blockSignals(True)
        self.to_unit_combo.blockSignals(True)

        self.from_unit_combo.clear()
        self.to_unit_combo.clear()

        self.from_unit_combo.addItems(units)
        self.to_unit_combo.addItems(units)

        if current_from in units:
            self.from_unit_combo.setCurrentText(current_from)
        if current_to in units:
            self.to_unit_combo.setCurrentText(current_to)

        self.from_unit_combo.blockSignals(False)
        self.to_unit_combo.blockSignals(False)

    def update_result(self, value, unit):
        """Affiche le résultat de la conversion"""
        # Formater le résultat avec un nombre approprié de décimales
        if value == 0:
            formatted = "0"
        elif abs(value) >= 1000 or abs(value) < 0.001:
            formatted = f"{value:.4e}".replace(".", ",")
        else:
            formatted = f"{value:,.6f}".replace(",", " ").replace(".", ",")
            formatted = formatted.rstrip("0").rstrip(",")

        self.result_value.setText(formatted)
        self.to_unit_combo.setCurrentText(unit)

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
        self.result_value.setText(f"Erreur: {message}")
        self.result_value.setStyleSheet("background-color: #ffdddd;")

    def on_convert_clicked(self):
        """Gère le clic sur le bouton de conversion"""
        value_text = self.input_value.text().replace(",", ".").strip()

        if not value_text:
            self.show_error("Veuillez entrer une valeur")
            return

        try:
            value = float(value_text)
            from_unit = self.from_unit_combo.currentText()
            to_unit = self.to_unit_combo.currentText()
            conv_type = self.conversion_type_combo.currentText()

            self.convert_requested.emit(value, from_unit, to_unit, conv_type)

        except ValueError:
            self.show_error("Veuillez entrer un nombre valide")

    def on_swap_clicked(self):
        """Échange les unités source et cible"""
        from_idx = self.from_unit_combo.currentIndex()
        to_idx = self.to_unit_combo.currentIndex()

        self.from_unit_combo.setCurrentIndex(to_idx)
        self.to_unit_combo.setCurrentIndex(from_idx)

        if self.input_value.text() and self.result_value.text():
            input_text = self.input_value.text()
            result_text = self.result_value.text()

            self.input_value.setText(result_text)
            self.result_value.setText(input_text)

        self.swap_units_requested.emit()

    def on_conversion_type_changed(self, conversion_type):
        """Gère le changement de type de conversion"""
        self.conversion_type_changed.emit(conversion_type)

    @property
    def current_conversion_type(self):
        return self.conversion_type_combo.currentText()

    @property
    def current_units(self):
        return (self.from_unit_combo.currentText(), self.to_unit_combo.currentText())
