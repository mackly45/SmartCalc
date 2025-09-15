from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDoubleValidator, QFont


class CurrencyView(QWidget):
    convert_requested = pyqtSignal(float, str, str)
    update_rates_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Titre
        title = QLabel("Convertisseur de devises")
        title.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #cdd6f4;
                margin-bottom: 20px;
            }
        """
        )
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Formulaire de conversion
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Montant à convertir
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("0.00")
        self.amount_edit.setValidator(QDoubleValidator(0, 999999999, 2, self))
        self.amount_edit.setStyleSheet(
            """
            QLineEdit {
                padding: 10px;
                border: 2px solid #45475a;
                border-radius: 5px;
                background: #1e1e2e;
                color: #cdd6f4;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #89b4fa;
            }
        """
        )

        # Sélecteurs de devise
        self.from_currency_combo = QComboBox()
        self.to_currency_combo = QComboBox()

        for combo in [self.from_currency_combo, self.to_currency_combo]:
            combo.setStyleSheet(
                """
                QComboBox {
                    padding: 8px;
                    border: 2px solid #45475a;
                    border-radius: 5px;
                    background: #1e1e2e;
                    color: #cdd6f4;
                    min-width: 200px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background: #1e1e2e;
                    color: #cdd6f4;
                    selection-background-color: #45475a;
                }
            """
            )

        # Bouton d'inversion des devises
        self.swap_button = QPushButton("⇅")
        self.swap_button.setFixedSize(40, 40)
        self.swap_button.setStyleSheet(
            """
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                border: none;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
        """
        )

        # Résultat de la conversion
        self.result_label = QLabel("0.00")
        self.result_label.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #a6e3a1;
                padding: 10px 0;
            }
        """
        )

        # Taux de change
        self.rate_label = QLabel("1.00 = 1.00")
        self.rate_label.setStyleSheet("color: #a6adc8;")

        # Bouton de conversion
        self.convert_button = QPushButton("Convertir")
        self.convert_button.setStyleSheet(
            """
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4c9fc;
            }
            QPushButton:disabled {
                background-color: #45475a;
                color: #6c7086;
            }
        """
        )

        # Layout pour les sélecteurs de devise
        currency_layout = QHBoxLayout()
        currency_layout.addWidget(self.from_currency_combo)
        currency_layout.addWidget(self.swap_button)
        currency_layout.addWidget(self.to_currency_combo)

        # Ajout des widgets au layout du formulaire
        form_layout.addRow("Montant:", self.amount_edit)
        form_layout.addRow("De:", currency_layout)
        form_layout.addRow("Résultat:", self.result_label)
        form_layout.addRow("Taux:", self.rate_label)

        layout.addLayout(form_layout)
        layout.addItem(
            QSpacerItem(
                20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Bouton de mise à jour des taux
        self.update_button = QPushButton("Mettre à jour les taux")
        self.update_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f9e2af;
                color: #1e1e2e;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #fae8b9;
            }
        """
        )

        # Barre d'état
        self.status_label = QLabel("Prêt")
        self.status_label.setStyleSheet("color: #a6adc8; font-style: italic;")

        # Layout pour les boutons du bas
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.convert_button)
        bottom_layout.addWidget(self.update_button)
        bottom_layout.addWidget(
            self.status_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addLayout(bottom_layout)

        # Connexion des signaux
        self.convert_button.clicked.connect(self.on_convert_clicked)
        self.swap_button.clicked.connect(self.on_swap_clicked)
        self.update_button.clicked.connect(self.update_rates_requested)
        self.amount_edit.returnPressed.connect(self.on_convert_clicked)

    def set_currencies(self, currencies):
        """Définit la liste des devises disponibles"""
        self.from_currency_combo.clear()
        self.to_currency_combo.clear()

        for code, name in currencies:
            self.from_currency_combo.addItem(f"{code} - {name}", code)
            self.to_currency_combo.addItem(f"{code} - {name}", code)

        # Définir des valeurs par défaut
        self.set_default_currencies()

    def set_default_currencies(self):
        """Définit les devises par défaut"""
        # Essayer de trouver EUR et USD
        eur_index = self.from_currency_combo.findData("EUR")
        usd_index = self.to_currency_combo.findData("USD")

        if eur_index >= 0:
            self.from_currency_combo.setCurrentIndex(eur_index)
        if usd_index >= 0:
            self.to_currency_combo.setCurrentIndex(usd_index)

    def get_conversion_data(self):
        """Récupère les données de conversion depuis l'interface"""
        try:
            amount = float(self.amount_edit.text() or "0")
            from_currency = self.from_currency_combo.currentData()
            to_currency = self.to_currency_combo.currentData()
            return amount, from_currency, to_currency
        except ValueError:
            return 0, None, None

    def set_conversion_result(self, result, rate=None):
        """Affiche le résultat de la conversion"""
        try:
            if result is not None:
                # Formater le résultat avec 2 décimales et des séparateurs de milliers
                formatted_result = f"{float(result):,.2f}"
                self.result_label.setText(formatted_result)

                if rate is not None:
                    from_curr = self.from_currency_combo.currentData()
                    to_curr = self.to_currency_combo.currentData()
                    if from_curr and to_curr:
                        self.rate_label.setText(
                            f"1 {from_curr} = {float(rate):,.6f} {to_curr}"
                        )
                    else:
                        self.rate_label.setText("Taux de change non disponible")
            else:
                self.result_label.setText("Erreur")
                self.rate_label.setText("Impossible d'effectuer la conversion")
        except Exception as e:
            print(f"Erreur lors de l'affichage du résultat: {e}")
            self.result_label.setText("Erreur")
            self.rate_label.setText("Une erreur est survenue")

    def on_convert_clicked(self):
        """Gestion du clic sur le bouton de conversion"""
        amount, from_curr, to_curr = self.get_conversion_data()
        if from_curr and to_curr:
            self.convert_requested.emit(amount, from_curr, to_curr)

    def on_swap_clicked(self):
        """Inverse les devises sélectionnées"""
        from_idx = self.from_currency_combo.currentIndex()
        to_idx = self.to_currency_combo.currentIndex()

        self.from_currency_combo.setCurrentIndex(to_idx)
        self.to_currency_combo.setCurrentIndex(from_idx)

        # Si un montant est saisi, on relance la conversion
        if self.amount_edit.text():
            self.on_convert_clicked()

    def set_status(self, message, is_error=False):
        """Affiche un message dans la barre d'état"""
        self.status_label.setText(message)
        if is_error:
            self.status_label.setStyleSheet("color: #f38ba8; font-style: italic;")
        else:
            self.status_label.setStyleSheet("color: #a6adc8; font-style: italic;")

    def set_loading(self, loading):
        """Active ou désactive l'état de chargement"""
        self.convert_button.setEnabled(not loading)
        self.update_button.setEnabled(not loading)
        self.swap_button.setEnabled(not loading)

        if loading:
            self.set_status("Traitement en cours...")
        else:
            self.set_status("Prêt")
