from PyQt6.QtCore import QObject, pyqtSignal


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
        self.current_type = None  # type de conversion courant
        self.connect_signals()

    def connect_signals(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur."""
        # La vue émet convert_requested(value, from_unit, to_unit, conv_type)
        if hasattr(self.view, 'convert_requested'):
            self.view.convert_requested.connect(self.convert_units)
        # Compat si certaines vues émettent encore convert_clicked(value, from_unit, to_unit)
        if hasattr(self.view, 'convert_clicked'):
            self.view.convert_clicked.connect(self.convert_units)
        self.view.category_changed.connect(self.on_category_changed)
        self.view.swap_units_requested.connect(self.swap_units)

    def convert_units(self, value, from_unit, to_unit, conv_type=None):
        try:
            conv_type = conv_type or self.current_type
            if not all([value, from_unit, to_unit, conv_type]):
                self.error_occurred.emit("Tous les champs sont obligatoires")
                return

            result = self.model.convert(float(value), from_unit, to_unit, conv_type)
            self.conversion_result.emit(result, to_unit)

        except ValueError:
            self.error_occurred.emit("Veuillez entrer une valeur numérique valide")
        except Exception as e:
            self.error_occurred.emit(f"Erreur de conversion: {str(e)}")

    def on_category_changed(self, category):
        """Gère le changement de catégorie de conversion."""
        self.current_category = category
        # Déduire un type de conversion simple = la catégorie elle-même
        self.current_type = category
        # Mettre à jour la liste des types si la vue le supporte
        types = [category] if category else []
        if hasattr(self.view, 'update_conversion_types'):
            self.view.update_conversion_types(types)
        if hasattr(self.view, 'set_conversion_type') and types:
            self.view.set_conversion_type(types[0])
        # Mettre à jour les unités disponibles
        units = self.model.get_units_for_category(category)
        self.view.set_units(units)

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
            # Harmonisé: l'input s'appelle value_input dans la vue
            if hasattr(self.view, 'value_input') and self.view.value_input.text():
                self.convert_units(
                    self.view.value_input.text(),
                    self.view.from_unit_combo.currentText(),
                    self.view.to_unit_combo.currentText(),
                    self.view.conversion_type_combo.currentText(),
                )

    def update_conversion_types(self, category):
        """Met à jour les types de conversion disponibles (simplifié)."""
        if not category:
            return
        types = [category]
        if hasattr(self.view, 'update_conversion_types'):
            self.view.update_conversion_types(types)
        self.current_type = types[0]
        if hasattr(self.view, 'set_conversion_type'):
            self.view.set_conversion_type(self.current_type)

    def update_units(self, category):
        """Met à jour les unités disponibles pour une catégorie."""
        if not category:
            return

        units = self.model.get_units_for_category(category)
        self.view.set_units(units)

    def set_categories(self, categories):
        """Définit les catégories disponibles."""
        self.view.set_categories(categories)

        if categories:
            self.view.category_combo.setCurrentIndex(0)
            self.current_category = categories[0]
            self.update_conversion_types(categories[0])
            self.update_units(categories[0])

    def set_conversion_type(self, conv_type: str):
        """Définit le type de conversion actuellement sélectionné."""
        if not conv_type:
            self.show_error("Type de conversion invalide")
            return

        self.current_type = conv_type

        # Si la vue peut réagir (combo ou affichage)
        if hasattr(self.view, "set_conversion_type"):
            self.view.set_conversion_type(conv_type)

    def show_error(self, message):
        """Affiche un message d'erreur."""
        self.error_occurred.emit(message)

    def clear(self):
        """Réinitialise l'interface."""
        self.view.clear()

    # Stubs d'initialisation/nettoyage utilisés par main.py
    def initialize_ui(self):
        """Initialise l'onglet convertisseur (catégories et unités)."""
        categories = self.model.get_categories()
        self.set_categories(categories)

    def cleanup(self):
        """Nettoyage éventuel (pas d'action pour l'instant)."""
        pass
