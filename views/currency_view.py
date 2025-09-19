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
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal


class CurrencyView(QWidget):
    """
    Vue pour le convertisseur de devises.
    Permet de convertir entre différentes devises en utilisant des taux de change à jour.
    """

    # Signaux
    convert_clicked = pyqtSignal(
        float, str, str
    )  # montant, devise_source, devise_cible
    update_rates_clicked = pyqtSignal()  # Demande de mise à jour des taux
    back_clicked = pyqtSignal()  # Retour à l'écran précédent

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        # Configuration de la fenêtre
        self.setWindowTitle("Convertisseur de devises")
        self.setMinimumSize(500, 400)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Bouton de retour
        self.back_button = QPushButton("← Retour au convertisseur")
        self.back_button.clicked.connect(self.back_clicked)

        # Groupe pour la sélection des devises
        currency_group = QGroupBox("Conversion de devises")
        form_layout = QGridLayout()

        # Montant à convertir
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant à convertir")
        self.amount_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Listes déroulantes pour les devises
        self.from_currency_combo = QComboBox()
        self.to_currency_combo = QComboBox()

        # Bouton d'inversion des devises
        self.swap_button = QPushButton("⇅")
        self.swap_button.setFixedWidth(40)
        self.swap_button.setToolTip("Inverser les devises")

        # Champ de résultat
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Bouton de conversion
        self.convert_button = QPushButton("Convertir")
        self.convert_button.setMinimumHeight(40)

        # Bouton de mise à jour des taux
        self.update_rates_button = QPushButton("Mettre à jour les taux")
        self.update_rates_button.setToolTip("Récupérer les derniers taux de change")

        # Date de dernière mise à jour
        self.last_update_label = QLabel("Dernière mise à jour: Inconnue")
        self.last_update_label.setStyleSheet("color: #666; font-style: italic;")

        # Taux de change actuel
        self.rate_label = QLabel("Taux: -")
        self.rate_label.setStyleSheet("font-weight: bold;")

        # Ajout des widgets au layout
        form_layout.addWidget(QLabel("Montant:"), 0, 0)
        form_layout.addWidget(self.amount_input, 0, 1)
        form_layout.addWidget(self.from_currency_combo, 0, 2)

        form_layout.addWidget(self.swap_button, 1, 1)

        form_layout.addWidget(QLabel("Résultat:"), 2, 0)
        form_layout.addWidget(self.result_display, 2, 1)
        form_layout.addWidget(self.to_currency_combo, 2, 2)

        form_layout.addWidget(self.rate_label, 3, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        currency_group.setLayout(form_layout)

        # Layout pour les boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_rates_button)
        button_layout.addWidget(self.convert_button)

        # Ajout des widgets au layout principal
        main_layout.addWidget(self.back_button)
        main_layout.addWidget(currency_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(
            self.last_update_label, alignment=Qt.AlignmentFlag.AlignRight
        )
        main_layout.addStretch()

        # Connexion des signaux
        self.convert_button.clicked.connect(self.on_convert_clicked)
        self.update_rates_button.clicked.connect(self.on_update_rates_clicked)
        self.swap_button.clicked.connect(self.on_swap_clicked)
        self.amount_input.returnPressed.connect(self.on_convert_clicked)

    def on_convert_clicked(self):
        """Gère le clic sur le bouton de conversion."""
        try:
            amount = float(self.amount_input.text().replace(" ", "").replace(",", "."))
            from_currency = self.from_currency_combo.currentText()
            to_currency = self.to_currency_combo.currentText()

            if from_currency and to_currency:
                self.convert_clicked.emit(amount, from_currency, to_currency)
        except ValueError:
            self.show_error("Veuillez entrer un montant valide")

    def on_update_rates_clicked(self):
        """Gère le clic sur le bouton de mise à jour des taux."""
        self.update_rates_clicked.emit()

    def on_swap_clicked(self):
        """Inverse les devises source et cible."""
        current_from = self.from_currency_combo.currentIndex()
        current_to = self.to_currency_combo.currentIndex()

        self.from_currency_combo.setCurrentIndex(current_to)
        self.to_currency_combo.setCurrentIndex(current_from)

        # Si une conversion a déjà été effectuée, on la relance
        if self.result_display.text() and self.amount_input.text():
            self.on_convert_clicked()

    def set_currencies(self, currencies):
        """Définit les devises disponibles."""
        current_from = self.from_currency_combo.currentText()
        current_to = self.to_currency_combo.currentText()

        self.from_currency_combo.clear()
        self.to_currency_combo.clear()

        if currencies:
            self.from_currency_combo.addItems(currencies)
            self.to_currency_combo.addItems(currencies)

            # Essayer de conserver la sélection précédente si possible
            if current_from in currencies and current_to in currencies:
                self.from_currency_combo.setCurrentText(current_from)
                self.to_currency_combo.setCurrentText(current_to)
            else:
                # Par défaut, sélectionner EUR et USD
                if "EUR" in currencies and "USD" in currencies:
                    self.from_currency_combo.setCurrentText("EUR")
                    self.to_currency_combo.setCurrentText("USD")

    def set_result(self, result):
        """Affiche le résultat de la conversion."""
        self.result_display.setText(
            f"{result:,.2f}".replace(",", " ").replace(".", ",")
        )

    def set_exchange_rate(self, rate, from_currency, to_currency):
        """Affiche le taux de change actuel."""
        self.rate_label.setText(f"1 {from_currency} = {rate:.6f} {to_currency}")

    def set_last_update(self, last_update):
        """Affiche la date de dernière mise à jour des taux."""
        self.last_update_label.setText(f"Dernière mise à jour: {last_update}")

    def show_error(self, message):
        """Affiche un message d'erreur."""
        QMessageBox.critical(self, "Erreur", message)

    def show_info(self, message):
        """Affiche un message d'information."""
        QMessageBox.information(self, "Information", message)

    def set_loading(self, loading):
        """Active ou désactive l'état de chargement."""
        self.convert_button.setEnabled(not loading)
        self.update_rates_button.setEnabled(not loading)
        self.amount_input.setReadOnly(loading)

        if loading:
            self.convert_button.setText("Chargement...")
            self.update_rates_button.setText("Mise à jour en cours...")
        else:
            self.convert_button.setText("Convertir")
            self.update_rates_button.setText("Mettre à jour les taux")
