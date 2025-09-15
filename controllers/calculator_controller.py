class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect view signals to controller methods
        self.view.button_clicked.connect(self.on_button_clicked)

        # Initialize the display
        self.update_display()

    def on_button_clicked(self, button_text):
        """Handle button clicks from the view"""
        if button_text.isdigit() or button_text == ".":
            if button_text == ".":
                self.model.add_decimal()
            else:
                self.model.append_number(button_text)
            self.update_display()

        elif button_text in "+-×÷":
            self.model.add_operator(button_text)
            self.update_display()

        elif button_text == "=":
            self.model.calculate()
            self.update_display()

        elif button_text == "C":
            self.model.clear()
            self.view.clear_display()

        elif button_text == "±":
            self.model.toggle_sign()
            self.update_display()

        elif button_text == "%":
            self.model.percentage()
            self.update_display()

    def update_display(self):
        """Update the view with the current model state"""
        self.view.update_display(self.model.current_value)
        self.view.update_expression(
            self.model.expression.replace("*", "×").replace("/", "÷")
        )

    def initialize_ui(self):
        """Initialise l'interface utilisateur avec les données du modèle"""
        # Mise à jour initiale de l'affichage
        self.update_display()

    def cleanup(self):
        """Nettoie les ressources"""
        # Nettoyage des ressources si nécessaire
        pass
