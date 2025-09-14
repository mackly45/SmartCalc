from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QGridLayout, QLabel, QSizePolicy,
                             QComboBox, QMenu, QMenuBar, QFrame, QScrollArea, QTabWidget, QMessageBox,
                             QListWidget, QListWidgetItem, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QAction, QIcon

class ScientificButton(QPushButton):
    """Bouton personnalisé pour la calculatrice scientifique"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(40, 40)
        
        # Style de base
        self.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
            QPushButton:checked {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
        """)

class ScientificView(QWidget):
    """Vue de la calculatrice scientifique"""
    expression_evaluated = pyqtSignal(str, str)  # expression, result
    function_pressed = pyqtSignal(str)  # function_name
    memory_operation = pyqtSignal(str, float)  # operation, value
    statistics_operation = pyqtSignal(str, object)  # operation, data
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Barre d'outils supérieure
        self.setup_toolbar(main_layout)
        
        # Zone d'affichage
        self.setup_display(main_layout)
        
        # Menu des fonctions
        self.setup_function_buttons(main_layout)
        
        # Clavier numérique et opérations
        self.setup_keypad(main_layout)
        
        # Zone des statistiques (cachée par défaut)
        self.setup_statistics_panel(main_layout)
        
        # Panneau d'historique (caché par défaut)
        self.setup_history_panel(main_layout)
        
        # Barre d'état
        self.setup_status_bar(main_layout)
        
        # Initialisation de l'état
        self.statistics_mode = False
        self.history_visible = False
        self.data_points = []
    
    def setup_toolbar(self, parent_layout):
        """Configure la barre d'outils supérieure"""
        toolbar = QHBoxLayout()
        toolbar.setSpacing(5)
        
        # Bouton pour activer/désactiver les statistiques
        self.stats_btn = QPushButton("📊 Statistiques")
        self.stats_btn.setCheckable(True)
        self.stats_btn.clicked.connect(self.toggle_statistics_mode)
        self.stats_btn.setStyleSheet("""
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                border: 1px solid #585b70;
                border-radius: 3px;
                padding: 5px 10px;
                margin-right: 5px;
            }
            QPushButton:checked {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
            QPushButton:checked:hover {
                background-color: #b4c9fc;
            }
        """)
        
        # Bouton pour afficher/masquer l'historique
        self.history_btn = QPushButton("📜 Historique")
        self.history_btn.setCheckable(True)
        self.history_btn.clicked.connect(self.toggle_history)
        self.history_btn.setStyleSheet("""
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                border: 1px solid #585b70;
                border-radius: 3px;
                padding: 5px 10px;
                margin-right: 5px;
            }
            QPushButton:checked {
                background-color: #f9e2af;
                color: #1e1e2e;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
            QPushButton:checked:hover {
                background-color: #fae8b9;
            }
        """)
        
        toolbar.addWidget(self.stats_btn)
        toolbar.addWidget(self.history_btn)
        toolbar.addStretch()
        
        parent_layout.addLayout(toolbar)
    
    def setup_display(self, parent_layout):
        """Configure la zone d'affichage"""
        # Cadre pour la zone d'affichage
        display_frame = QFrame()
        display_frame.setFrameShape(QFrame.Shape.StyledPanel)
        display_frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        display_layout = QVBoxLayout(display_frame)
        display_layout.setContentsMargins(5, 5, 5, 5)
        display_layout.setSpacing(5)
        
        # Affichage de l'expression
        self.expression_display = QLineEdit()
        self.expression_display.setReadOnly(True)
        self.expression_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_display.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                color: #a6adc8;
                font-size: 14px;
                padding: 5px;
            }
        """)
        
        # Affichage du résultat
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_display.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                color: #cdd6f4;
                font-size: 24px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        
        display_layout.addWidget(self.expression_display)
        display_layout.addWidget(self.result_display)
        
        parent_layout.addWidget(display_frame)
    
    def setup_function_buttons(self, parent_layout):
        """Configure les boutons de fonction"""
        # Barre d'onglets pour les différentes catégories de fonctions
        self.function_tabs = QTabWidget()
        self.function_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #45475a;
                border-radius: 5px;
                background: #1e1e2e;
            }
            QTabBar::tab {
                background: #313244;
                color: #cdd6f4;
                padding: 8px 15px;
                border: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #45475a;
                border-bottom: 2px solid #89b4fa;
            }
            QTabBar::tab:hover:!selected {
                background: #585b70;
            }
        """)
        
        # Onglet des fonctions mathématiques de base
        math_tab = QWidget()
        math_layout = QGridLayout(math_tab)
        math_layout.setContentsMargins(5, 5, 5, 5)
        math_layout.setSpacing(5)
        
        # Boutons des fonctions mathématiques
        math_functions = [
            ('sin', 'cos', 'tan', '(', ')'),
            ('asin', 'acos', 'atan', '√', '^'),
            ('log', 'ln', 'exp', 'π', 'e'),
            ('sinh', 'cosh', 'tanh', 'x²', 'x³')
        ]
        
        for row, funcs in enumerate(math_functions):
            for col, func in enumerate(funcs):
                btn = ScientificButton(func)
                btn.clicked.connect(lambda checked, f=func: self.on_function_clicked(f))
                math_layout.addWidget(btn, row, col)
        
        # Onglet des constantes et autres fonctions
        const_tab = QWidget()
        const_layout = QGridLayout(const_tab)
        const_layout.setContentsMargins(5, 5, 5, 5)
        const_layout.setSpacing(5)
        
        constantes = [
            ('π', 'e', 'φ', 'γ'),
            ('∞', '°', 'mod', '!')
        ]
        
        for row, consts in enumerate(constantes):
            for col, const in enumerate(consts):
                btn = ScientificButton(const)
                btn.clicked.connect(lambda checked, c=const: self.on_constant_clicked(c))
                const_layout.addWidget(btn, row, col)
        
        # Ajout des onglets
        self.function_tabs.addTab(math_tab, "Fonctions")
        self.function_tabs.addTab(const_tab, "Constantes")
        
        parent_layout.addWidget(self.function_tabs)
    
    def setup_keypad(self, parent_layout):
        """Configure le clavier numérique et les opérations"""
        keypad_frame = QFrame()
        keypad_layout = QHBoxLayout(keypad_frame)
        keypad_layout.setContentsMargins(0, 0, 0, 0)
        keypad_layout.setSpacing(5)
        
        # Clavier numérique
        num_grid = QGridLayout()
        num_grid.setContentsMargins(0, 0, 0, 0)
        num_grid.setSpacing(5)
        
        # Boutons numériques et opérations
        buttons = [
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', '⌫'),
            ('1', '2', '3', '-', '±'),
            ('0', '.', '=', '+', '%')
        ]
        
        for row, row_buttons in enumerate(buttons):
            for col, text in enumerate(row_buttons):
                btn = ScientificButton(text)
                
                # Style spécial pour le bouton égal
                if text == '=':
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #a6e3a1;
                            color: #1e1e2e;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #b4e9b0;
                        }
                    """)
                    btn.clicked.connect(self.on_equals_clicked)
                # Style pour les boutons de chiffres
                elif text.isdigit() or text == '.':
                    btn.clicked.connect(lambda checked, t=text: self.on_digit_clicked(t))
                # Style pour les boutons d'opérations
                elif text in ['+', '-', '*', '/']:
                    btn.clicked.connect(lambda checked, t=text: self.on_operator_clicked(t))
                # Gestion des boutons spéciaux
                elif text == 'C':
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f38ba8;
                            color: #1e1e2e;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #f5a9b8;
                        }
                    """)
                    btn.clicked.connect(self.on_clear_clicked)
                elif text == '⌫':
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f9e2af;
                            color: #1e1e2e;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #fae8b9;
                        }
                    """)
                    btn.clicked.connect(self.on_backspace_clicked)
                elif text == '±':
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #89b4fa;
                            color: #1e1e2e;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #b4c9fc;
                        }
                    """)
                    btn.clicked.connect(self.on_plus_minus_clicked)
                elif text == '%':
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #89b4fa;
                            color: #1e1e2e;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #b4c9fc;
                        }
                    """)
                    btn.clicked.connect(self.on_percent_clicked)
                
                num_grid.addWidget(btn, row, col)
        
        keypad_layout.addLayout(num_grid)
        parent_layout.addWidget(keypad_frame)
    
    def setup_status_bar(self, parent_layout):
        """Configure la barre d'état"""
        status_bar = QHBoxLayout()
        status_bar.setContentsMargins(0, 5, 0, 0)
        
        # Mode d'angle
        self.angle_mode = QComboBox()
        self.angle_mode.addItems(['DEG', 'RAD', 'GRAD'])
        self.angle_mode.setStyleSheet("""
            QComboBox {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 3px 5px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #313244;
                color: #cdd6f4;
                selection-background-color: #45475a;
            }
        """)
        
        # Affichage de la mémoire
        self.memory_status = QLabel("Mémoire: 0")
        self.memory_status.setStyleSheet("color: #a6adc8;")
        
        status_bar.addWidget(QLabel("Mode d'angle:"))
        status_bar.addWidget(self.angle_mode)
        status_bar.addStretch()
        status_bar.addWidget(self.memory_status)
        
        parent_layout.addLayout(status_bar)
    
    def setup_statistics_panel(self, parent_layout):
        """Configure le panneau des statistiques"""
        # Cadre principal pour les statistiques
        self.stats_frame = QFrame()
        self.stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.stats_frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border: 1px solid #45475a;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #cdd6f4;
            }
            QLineEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        stats_layout = QVBoxLayout(self.stats_frame)
        stats_layout.setSpacing(10)
        
        # Titre
        title = QLabel("Statistiques")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        stats_layout.addWidget(title)
        
        # Zone de saisie des données
        data_layout = QHBoxLayout()
        data_layout.addWidget(QLabel("Données (séparées par des virgules):"))
        
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Ex: 1, 2, 3, 4, 5")
        data_layout.addWidget(self.data_input)
        
        add_btn = QPushButton("Ajouter")
        add_btn.clicked.connect(self.add_data_points)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #a6e3a1;
                color: #1e1e2e;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #b4e9b0;
            }
        """)
        data_layout.addWidget(add_btn)
        
        clear_btn = QPushButton("Effacer")
        clear_btn.clicked.connect(self.clear_data_points)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #f5a9b8;
            }
        """)
        data_layout.addWidget(clear_btn)
        
        stats_layout.addLayout(data_layout)
        
        # Affichage des résultats
        results_layout = QGridLayout()
        results_layout.setHorizontalSpacing(20)
        results_layout.setVerticalSpacing(5)
        
        # Fonctions de base
        results_layout.addWidget(QLabel("Moyenne:"), 0, 0)
        self.mean_label = QLabel("-")
        results_layout.addWidget(self.mean_label, 0, 1)
        
        results_layout.addWidget(QLabel("Médiane:"), 1, 0)
        self.median_label = QLabel("-")
        results_layout.addWidget(self.median_label, 1, 1)
        
        results_layout.addWidget(QLabel("Mode:"), 2, 0)
        self.mode_label = QLabel("-")
        results_layout.addWidget(self.mode_label, 2, 1)
        
        results_layout.addWidget(QLabel("Écart-type (population):"), 0, 2)
        self.std_dev_label = QLabel("-")
        results_layout.addWidget(self.std_dev_label, 0, 3)
        
        results_layout.addWidget(QLabel("Variance (population):"), 1, 2)
        self.variance_label = QLabel("-")
        results_layout.addWidget(self.variance_label, 1, 3)
        
        # Bouton pour calculer les statistiques
        calc_btn = QPushButton("Calculer les statistiques")
        calc_btn.clicked.connect(self.calculate_statistics)
        calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                padding: 8px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4c9fc;
            }
        """)
        
        stats_layout.addLayout(results_layout)
        stats_layout.addWidget(calc_btn)
        
        # Cacher le panneau par défaut
        self.stats_frame.hide()
        parent_layout.addWidget(self.stats_frame)
    
    def setup_history_panel(self, parent_layout):
        """Configure le panneau d'historique"""
        # Cadre principal pour l'historique
        self.history_frame = QFrame()
        self.history_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.history_frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border: 1px solid #45475a;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: none;
                padding: 5px;
                font-family: monospace;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #313244;
            }
            QListWidget::item:selected {
                background-color: #45475a;
            }
            QListWidget::item:hover {
                background-color: #313244;
            }
        """)
        
        history_layout = QVBoxLayout(self.history_frame)
        history_layout.setContentsMargins(5, 5, 5, 5)
        history_layout.setSpacing(5)
        
        # Barre d'outils de l'historique
        history_toolbar = QHBoxLayout()
        
        title = QLabel("Historique des calculs")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        history_toolbar.addWidget(title)
        
        history_toolbar.addStretch()
        
        # Bouton pour effacer l'historique
        clear_btn = QPushButton("Effacer")
        clear_btn.clicked.connect(self.clear_history)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                padding: 3px 8px;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #f5a9b8;
            }
        """)
        
        # Bouton pour exporter l'historique
        export_btn = QPushButton("Exporter")
        export_btn.clicked.connect(self.export_history)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                padding: 3px 8px;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                margin-left: 5px;
            }
            QPushButton:hover {
                background-color: #b4c9fc;
            }
        """)
        
        history_toolbar.addWidget(clear_btn)
        history_toolbar.addWidget(export_btn)
        
        # Liste des calculs précédents
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.history_list.itemDoubleClicked.connect(self.use_history_item)
        
        # Bouton pour effacer la sélection
        self.clear_selection_btn = QPushButton("Effacer la sélection")
        self.clear_selection_btn.setEnabled(False)
        self.clear_selection_btn.clicked.connect(self.clear_selection)
        self.clear_selection_btn.setStyleSheet("""
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                padding: 5px;
                border: 1px solid #585b70;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:enabled {
                background-color: #f38ba8;
                color: #1e1e2e;
            }
            QPushButton:enabled:hover {
                background-color: #f5a9b8;
            }
        """)
        
        # Mettre à jour l'état du bouton de suppression
        self.history_list.itemSelectionChanged.connect(
            lambda: self.clear_selection_btn.setEnabled(
                len(self.history_list.selectedItems()) > 0
            )
        )
        
        history_layout.addLayout(history_toolbar)
        history_layout.addWidget(self.history_list)
        history_layout.addWidget(self.clear_selection_btn)
        
        # Cacher le panneau par défaut
        self.history_frame.hide()
        parent_layout.addWidget(self.history_frame)
    
    # Gestionnaires d'événements
    def on_digit_clicked(self, digit):
        """Gère le clic sur un bouton numérique"""
        current = self.result_display.text()
        if current == '0' or current == 'Erreur':
            self.result_display.setText(digit)
        else:
            self.result_display.setText(current + digit)
    
    def on_operator_clicked(self, op):
        """Gère le clic sur un opérateur"""
        current = self.result_display.text()
        if current == 'Erreur':
            self.result_display.setText('0' + op)
        else:
            # Vérifier si le dernier caractère est déjà un opérateur
            if current and current[-1] in '+-*/':
                self.result_display.setText(current[:-1] + op)
            else:
                self.result_display.setText(current + op)
    
    def on_function_clicked(self, func):
        """Gère le clic sur une fonction mathématique"""
        current = self.result_display.text()
        if current == 'Erreur':
            self.result_display.clear()
            current = ''
        
        # Gestion des fonctions spéciales
        if func == 'x²':
            self.result_display.setText(f"({current})**2")
        elif func == 'x³':
            self.result_display.setText(f"({current})**3")
        elif func == '√':
            self.result_display.setText(f"sqrt({current})")
        elif func == '^':
            self.result_display.setText(current + '^')
        else:
            # Pour les fonctions standard (sin, cos, tan, etc.)
            self.result_display.setText(f"{func}({current})")
    
    def on_constant_clicked(self, const):
        """Gère le clic sur une constante mathématique"""
        current = self.result_display.text()
        if current == '0' or current == 'Erreur':
            self.result_display.setText(const)
        else:
            self.result_display.setText(current + const)
    
    def on_equals_clicked(self):
        """Évalue l'expression actuelle"""
        expression = self.result_display.text()
        if expression and expression != 'Erreur':
            try:
                # Émettre le signal pour évaluer l'expression
                self.expression_evaluated.emit(expression, '')
            except Exception as e:
                print(f"Erreur d'évaluation: {e}")
                self.result_display.setText('Erreur')
    
    def on_clear_clicked(self):
        """Efface l'affichage"""
        self.result_display.clear()
        self.expression_display.clear()
    
    def on_backspace_clicked(self):
        """Supprime le dernier caractère"""
        current = self.result_display.text()
        if current != 'Erreur':
            self.result_display.setText(current[:-1] if current else '0')
    
    def on_plus_minus_clicked(self):
        """Inverse le signe de la valeur actuelle"""
        current = self.result_display.text()
        if current and current != 'Erreur':
            if current[0] == '-':
                self.result_display.setText(current[1:])
            else:
                self.result_display.setText('-' + current)
    
    def on_percent_clicked(self):
        """Calcule le pourcentage de la valeur actuelle"""
        current = self.result_display.text()
        if current and current != 'Erreur':
            try:
                value = float(current) / 100
                self.result_display.setText(str(value))
            except ValueError:
                self.result_display.setText('Erreur')
    
    def set_result(self, result):
        """Définit le résultat du calcul"""
        self.result_display.setText(str(result))
    
    def set_expression(self, expression):
        """Définit l'expression actuelle"""
        self.expression_display.setText(expression)
    
    def update_memory_display(self, value):
        """Met à jour l'affichage de la mémoire"""
        self.memory_status.setText(f"Mémoire: {value}")
    
    def get_angle_mode(self):
        """Retourne le mode d'angle actuel"""
        return self.angle_mode.currentText()

    # Méthodes pour les statistiques
    def add_data_points(self):
        """Ajoute des points de données à partir de la zone de saisie"""
        try:
            text = self.data_input.text().strip()
            if not text:
                return
                
            # Émettre le signal pour ajouter les données
            self.statistics_operation.emit('add', text)
            self.data_input.clear()
            
            # Mettre à jour l'affichage
            if hasattr(self, 'controller'):
                self.controller.update_statistics_display()
            
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des nombres valides séparés par des virgules.")
    
    def clear_data_points(self):
        """Efface tous les points de données"""
        self.statistics_operation.emit('clear', None)
        if hasattr(self, 'controller'):
            self.controller.update_statistics_display()
    
    def calculate_statistics(self):
        """Calcule et affiche les statistiques des données"""
        if not hasattr(self, 'data_points') or not self.data_points:
            QMessageBox.information(self, "Information", "Aucune donnée à analyser.")
            return
            
        try:
            # Demander le calcul des statistiques via le contrôleur
            results = self.controller.handle_statistics('calculate')
            if results is None:
                raise ValueError("Impossible de calculer les statistiques")
                
            # Mettre à jour l'affichage
            self.controller.update_statistics_display()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du calcul des statistiques: {str(e)}")
    
    def toggle_statistics_mode(self):
        """Active ou désactive le mode statistiques"""
        self.statistics_mode = not self.statistics_mode
        self.stats_frame.setVisible(self.statistics_mode)
        
        # Si on désactive le mode statistiques, on efface les données
        if not self.statistics_mode:
            self.clear_data_points()
        
        # Ajuster la visibilité des autres éléments
        self.function_tabs.setVisible(not self.statistics_mode)
        
        # Mettre à jour le style du bouton
        self.stats_btn.setChecked(self.statistics_mode)

    # Méthodes pour gérer l'historique
    def update_history_display(self):
        """Met à jour l'affichage de l'historique"""
        self.history_list.clear()
        
        if not hasattr(self, 'controller') or not hasattr(self.controller.model, 'history'):
            return
            
        history = self.controller.model.get_history()
        
        for entry in reversed(history):
            # Formater la date et l'heure
            timestamp = entry['timestamp'].strftime('%H:%M:%S')
            expression = entry['expression']
            result = entry['result']
            
            # Créer un élément personnalisé
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, entry)
            
            # Widget personnalisé pour afficher l'entrée d'historique
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(2)
            
            # Ligne d'en-tête avec l'horodatage
            header = QHBoxLayout()
            time_label = QLabel(timestamp)
            time_label.setStyleSheet("color: #a6adc8; font-size: 10px;")
            header.addWidget(time_label)
            header.addStretch()
            
            # Expression et résultat
            expr_label = QLabel(expression)
            expr_label.setStyleSheet("color: #cdd6f4;")
            
            result_label = QLabel(f"= {result}")
            result_label.setStyleSheet("color: #a6e3a1; font-weight: bold;")
            
            # Ajouter les widgets au layout
            layout.addLayout(header)
            layout.addWidget(expr_label)
            layout.addWidget(result_label)
            
            # Définir la taille de l'élément
            item.setSizeHint(widget.sizeHint())
            
            # Ajouter l'élément à la liste
            self.history_list.addItem(item)
            self.history_list.setItemWidget(item, widget)
    
    def toggle_history(self):
        """Affiche ou masque le panneau d'historique"""
        self.history_visible = not self.history_visible
        self.history_frame.setVisible(self.history_visible)
        self.history_btn.setChecked(self.history_visible)
        
        # Mettre à jour l'affichage si on affiche l'historique
        if self.history_visible:
            self.update_history_display()
    
    def use_history_item(self, item):
        """Utilise un élément de l'historique dans le calcul actuel"""
        entry = item.data(Qt.ItemDataRole.UserRole)
        if entry and 'expression' in entry:
            self.result_display.setText(entry['expression'])
    
    def clear_history(self):
        """Efface tout l'historique"""
        if hasattr(self, 'controller') and hasattr(self.controller.model, 'clear_history'):
            self.controller.model.clear_history()
            self.update_history_display()
    
    def clear_selection(self):
        """Efface l'élément sélectionné de l'historique"""
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            return
            
        item = selected_items[0]
        row = self.history_list.row(item)
        
        # Supprimer l'élément du modèle
        if hasattr(self, 'controller') and hasattr(self.controller.model, 'history'):
            # L'historique est affiché à l'envers (du plus récent au plus ancien)
            history = self.controller.model.get_history()
            if 0 <= row < len(history):
                # Convertir l'index car l'affichage est inversé
                actual_index = len(history) - 1 - row
                del self.controller.model.history[actual_index]
                self.update_history_display()
    
    def export_history(self):
        """Exporte l'historique dans un fichier"""
        if not hasattr(self, 'controller') or not hasattr(self.controller.model, 'save_history_to_file'):
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter l'historique",
            "",
            "Fichiers texte (*.txt);;Tous les fichiers (*)"
        )
        
        if file_path:
            if not file_path.endswith('.txt'):
                file_path += '.txt'
                
            if self.controller.model.save_history_to_file(file_path):
                QMessageBox.information(self, "Succès", "L'historique a été exporté avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'exporter l'historique.")
