from PyQt6.QtCore import QObject, pyqtSignal
from models.conversion_model import ConversionModel, ConversionType


class ConversionController(QObject):
    """
    Contrôleur pour gérer les conversions d'unités.
    Gère les interactions entre la vue et le modèle.
    """

    # Signaux pour la mise à jour de l'interface utilisateur
    conversion_result = pyqtSignal(float, str)  # Émet le résultat et l'unité cible
    units_updated = pyqtSignal(list)  # Émet la liste des unités disponibles
    error_occurred = pyqtSignal(str)  # Émet les messages d'erreur
    history_updated = pyqtSignal(list)  # Émet l'historique des conversions

    def __init__(self):
        super().__init__()
        self.model = ConversionModel()
        self._current_conversion_type = ConversionType.LENGTH.value
        self._from_unit = "m"  # Unité par défaut
        self._to_unit = "cm"  # Unité cible par défaut
        self._history = []

    def set_conversion_type(self, conversion_type: str) -> None:
        """Définit le type de conversion actuel (longueur, masse, etc.)"""
        if conversion_type in [t.value for t in ConversionType]:
            self._current_conversion_type = conversion_type
            # Mettre à jour les unités disponibles
            units = self.model.get_units(conversion_type)
            self.units_updated.emit(units)

            # Définir des valeurs par défaut appropriées
            if units:
                self._from_unit = units[0]
                self._to_unit = units[1] if len(units) > 1 else units[0]
        else:
            self.error_occurred.emit("Type de conversion non valide")

    def set_units(self, from_unit: str, to_unit: str) -> None:
        """Définit les unités source et cible"""
        available_units = self.model.get_units(self._current_conversion_type)
        if from_unit in available_units and to_unit in available_units:
            self._from_unit = from_unit
            self._to_unit = to_unit
        else:
            self.error_occurred.emit("Unités non valides pour ce type de conversion")

    def convert(self, value: str) -> None:
        """Effectue la conversion et émet le résultat"""
        try:
            # Vérifier si la valeur d'entrée est valide
            if not value:
                self.error_occurred.emit("Veuillez entrer une valeur à convertir")
                return

            numeric_value = float(value)

            # Effectuer la conversion
            result = self.model.convert(
                numeric_value,
                self._from_unit,
                self._to_unit,
                self._current_conversion_type,
            )

            if result is not None:
                # Mettre à jour l'historique
                self._add_to_history(numeric_value, result)
                # Émettre le résultat
                self.conversion_result.emit(result, self._to_unit)
            else:
                self.error_occurred.emit("Erreur lors de la conversion")

        except ValueError:
            self.error_occurred.emit("Veuillez entrer un nombre valide")

    def _add_to_history(self, from_value: float, to_value: float) -> None:
        """Ajoute une conversion à l'historique"""
        entry = {
            "type": self._current_conversion_type,
            "from_value": from_value,
            "from_unit": self._from_unit,
            "to_value": to_value,
            "to_unit": self._to_unit,
            "timestamp": "now",  # À remplacer par datetime.now()
        }
        self._history.insert(0, entry)
        # Limiter l'historique aux 10 dernières entrées
        self._history = self._history[:10]
        # Mettre à jour la vue
        self.history_updated.emit(self._history)

    def get_conversion_types(self) -> list:
        """Retourne la liste des types de conversion disponibles"""
        return self.model.get_conversion_types()

    def get_current_units(self) -> tuple:
        """Retourne les unités actuellement sélectionnées"""
        return self._from_unit, self._to_unit

    def get_available_units(self) -> list:
        """Retourne la liste des unités disponibles pour le type de conversion actuel"""
        return self.model.get_units(self._current_conversion_type)

    def swap_units(self) -> None:
        """Échange les unités source et cible"""
        self._from_unit, self._to_unit = self._to_unit, self._from_unit
        # Émettre le signal pour mettre à jour l'interface
        self.units_updated.emit(self.get_available_units())

        # Si une conversion a déjà été effectuée, on relance la conversion
        if hasattr(self, "_last_value"):
            self.convert(str(self._last_value))

    def cleanup(self):
        """Nettoyage avant la fermeture de l'application"""
        # Sauvegarder l'historique si nécessaire
        pass
