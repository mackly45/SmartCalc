from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, List, Optional


class ConversionController(QObject):
    """
    Contrôleur pour les conversions d'unités.
    Gère la logique de conversion entre différentes unités de mesure.
    """

    # Signaux
    conversion_result = pyqtSignal(float, str)  # valeur, unité
    error_occurred = pyqtSignal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.current_category = None
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur."""
        self.view.convert_clicked.connect(self.convert_units)
        self.view.category_changed.connect(self.on_category_changed)
        self.view.swap_units_requested.connect(self.swap_units)

    def on_category_changed(self, category):
        """Gère le changement de catégorie de conversion."""
        self.current_category = category
        units = self.model.get_units_for_category(category)
        self.view.set_units(units)

    def convert_units(self, value, from_unit, to_unit, conv_type):
        """
        Convertit une valeur d'une unité à une autre.

        Args:
            value: La valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
            conv_type: Type de conversion
        """
        try:
            if not all([value, from_unit, to_unit, conv_type]):
                self.error_occurred.emit("Tous les champs sont obligatoires")
                return

            result = self.model.convert(float(value), from_unit, to_unit, conv_type)
            self.conversion_result.emit(result, to_unit)

        except ValueError as e:
            self.error_occurred.emit("Veuillez entrer une valeur numérique valide")
        except Exception as e:
            self.error_occurred.emit(f"Erreur de conversion: {str(e)}")

    def swap_units(self):
        """Inverse les unités source et cible."""
        if (
            self.view.from_unit_combo.currentText()
            and self.view.to_unit_combo.currentText()
        ):
            from_idx = self.view.from_unit_combo.currentIndex()
            to_idx = self.view.to_unit_combo.currentIndex()

            self.view.from_unit_combo.setCurrentIndex(to_idx)
            self.view.to_unit_combo.setCurrentIndex(from_idx)

            # Si une valeur est présente, on relance la conversion
            if self.view.amount_input.text():
                self.convert_units(
                    self.view.amount_input.text(),
                    self.view.from_unit_combo.currentText(),
                    self.view.to_unit_combo.currentText(),
                    self.view.conversion_type_combo.currentText(),
                )

    def update_conversion_types(self, category):
        """Met à jour les types de conversion disponibles."""
        if not category:
            return

        conv_types = self.model.get_conversion_types(category)
        self.view.update_conversion_types(conv_types)

        if conv_types:
            self.view.conversion_type_combo.setCurrentIndex(0)

    def update_units(self, category):
        """Met à jour les unités disponibles pour une catégorie."""
        if not category:
            return

        units = self.model.get_units_for_category(category)
        self.view.update_units(units)

    def set_categories(self, categories):
        """Définit les catégories disponibles."""
        self.view.set_categories(categories)

        if categories:
            self.view.category_combo.setCurrentIndex(0)
            self.current_category = categories[0]
            self.update_conversion_types(categories[0])
            self.update_units(categories[0])

    def show_error(self, message):
        """Affiche un message d'erreur."""
        self.error_occurred.emit(message)

    def clear(self):
        """Réinitialise l'interface."""
        self.view.clear()
