from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QComboBox, QFileDialog, QMessageBox,
                             QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
                             QSplitter, QSizePolicy, QTextEdit, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPen, QPainter, QPixmap
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import sympy as sp

class MplCanvas(FigureCanvas):
    """Widget pour afficher les graphiques matplotlib"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1e1e2e')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#1e1e2e')
        
        # Style du graphique
        self.axes.tick_params(axis='x', colors='#cdd6f4')
        self.axes.tick_params(axis='y', colors='#cdd6f4')
        self.axes.spines['bottom'].set_color('#585b70')
        self.axes.spines['top'].set_color('#585b70') 
        self.axes.spines['right'].set_color('#585b70')
        self.axes.spines['left'].set_color('#585b70')
        self.axes.xaxis.label.set_color('#cdd6f4')
        self.axes.yaxis.label.set_color('#cdd6f4')
        self.axes.title.set_color('#cdd6f4')
        
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.updateGeometry()


class AdvancedView(QWidget):
    """Vue avancée pour les graphiques, matrices et factorisation"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Création des onglets
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
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
        
        # Onglet Graphiques
        self.setup_graph_tab()
        
        # Onglet Matrices
        self.setup_matrix_tab()
        
        # Onglet Factorisation
        self.setup_factorization_tab()
        
        main_layout.addWidget(self.tabs)
    
    def setup_graph_tab(self):
        """Configure l'onglet des graphiques"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Zone supérieure : Contrôles du graphique
        controls_layout = QHBoxLayout()
        
        # Sélection de la fonction
        func_group = QGroupBox("Fonction")
        func_layout = QFormLayout()
        
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ex: sin(x), x^2, exp(x)")
        func_layout.addRow("f(x) =", self.function_input)
        
        # Plage de x
        self.x_min = QDoubleSpinBox()
        self.x_min.setRange(-1000, 1000)
        self.x_min.setValue(-10)
        self.x_max = QDoubleSpinBox()
        self.x_max.setRange(-1000, 1000)
        self.x_max.setValue(10)
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(self.x_min)
        range_layout.addWidget(QLabel("≤ x ≤"))
        range_layout.addWidget(self.x_max)
        func_layout.addRow("Intervalle x:", range_layout)
        
        # Options du graphique
        self.show_grid = QCheckBox("Afficher la grille")
        self.show_grid.setChecked(True)
        func_layout.addRow(self.show_grid)
        
        self.show_legend = QCheckBox("Afficher la légende")
        self.show_legend.setChecked(True)
        func_layout.addRow(self.show_legend)
        
        # Bouton de tracé
        plot_btn = QPushButton("Tracer")
        plot_btn.clicked.connect(self.plot_function)
        plot_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4c9fc;
            }
        """)
        
        func_layout.addRow(plot_btn)
        func_group.setLayout(func_layout)
        
        # Options d'export
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout()
        
        export_btn = QPushButton("Exporter le graphique")
        export_btn.clicked.connect(self.export_plot)
        export_btn.setStyleSheet("""
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
        
        export_layout.addWidget(export_btn)
        export_group.setLayout(export_layout)
        
        # Ajout des contrôles au layout
        controls_layout.addWidget(func_group)
        controls_layout.addWidget(export_group)
        
        # Zone du graphique
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        
        # Zone de démonstration
        demo_group = QGroupBox("Démonstration")
        demo_layout = QVBoxLayout()
        
        self.demo_text = QTextEdit()
        self.demo_text.setReadOnly(True)
        self.demo_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 5px;
                font-family: monospace;
            }
        """)
        
        demo_layout.addWidget(self.demo_text)
        demo_group.setLayout(demo_layout)
        
        # Splitter pour redimensionner le graphique et la démo
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.canvas)
        splitter.addWidget(demo_group)
        splitter.setSizes([400, 150])
        
        # Ajout au layout principal
        layout.addLayout(controls_layout)
        layout.addWidget(splitter)
        
        # Ajout de l'onglet
        self.tabs.addTab(tab, "Graphiques")
    
    def setup_matrix_tab(self):
        """Configure l'onglet des matrices"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Contrôles des matrices
        matrix_controls = QHBoxLayout()
        
        # Sélection de la taille
        size_group = QGroupBox("Taille des matrices")
        size_layout = QHBoxLayout()
        
        self.matrix_rows = QSpinBox()
        self.matrix_rows.setRange(1, 10)
        self.matrix_rows.setValue(3)
        self.matrix_cols = QSpinBox()
        self.matrix_cols.setRange(1, 10)
        self.matrix_cols.setValue(3)
        
        size_layout.addWidget(QLabel("Lignes:"))
        size_layout.addWidget(self.matrix_rows)
        size_layout.addStretch()
        size_layout.addWidget(QLabel("Colonnes:"))
        size_layout.addWidget(self.matrix_cols)
        
        # Mise à jour des matrices lors du changement de taille
        self.matrix_rows.valueChanged.connect(self.update_matrix_size)
        self.matrix_cols.valueChanged.connect(self.update_matrix_size)
        
        size_group.setLayout(size_layout)
        
        # Opérations sur les matrices
        ops_group = QGroupBox("Opérations")
        ops_layout = QVBoxLayout()
        
        # Boutons d'opérations
        add_btn = QPushButton("Addition (A + B)")
        sub_btn = QPushButton("Soustraction (A - B)")
        mul_btn = QPushButton("Multiplication (A × B)")
        det_btn = QPushButton("Déterminant")
        inv_btn = QPushButton("Inverse")
        trans_btn = QPushButton("Transposée")
        
        # Style des boutons
        button_style = """
            QPushButton {
                text-align: left;
                padding: 5px 10px;
                margin: 2px 0;
                border: 1px solid #45475a;
                border-radius: 3px;
                background-color: #313244;
                color: #cdd6f4;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """
        
        for btn in [add_btn, sub_btn, mul_btn, det_btn, inv_btn, trans_btn]:
            btn.setStyleSheet(button_style)
            ops_layout.addWidget(btn)
        
        ops_group.setLayout(ops_layout)
        
        # Ajout des contrôles
        matrix_controls.addWidget(size_group)
        matrix_controls.addWidget(ops_group)
        
        # Zone des matrices
        matrix_area = QHBoxLayout()
        
        # Matrice A
        a_group = QGroupBox("Matrice A")
        a_layout = QVBoxLayout()
        self.matrix_a = QTableWidget()
        self.matrix_a.setRowCount(3)
        self.matrix_a.setColumnCount(3)
        a_layout.addWidget(self.matrix_a)
        a_group.setLayout(a_layout)
        
        # Matrice B
        b_group = QGroupBox("Matrice B")
        b_layout = QVBoxLayout()
        self.matrix_b = QTableWidget()
        self.matrix_b.setRowCount(3)
        self.matrix_b.setColumnCount(3)
        b_layout.addWidget(self.matrix_b)
        b_group.setLayout(b_layout)
        
        # Matrice résultat
        result_group = QGroupBox("Résultat")
        result_layout = QVBoxLayout()
        self.matrix_result = QTableWidget()
        self.matrix_result.setRowCount(3)
        self.matrix_result.setColumnCount(3)
        result_layout.addWidget(self.matrix_result)
        result_group.setLayout(result_layout)
        
        # Style des tableaux
        for table in [self.matrix_a, self.matrix_b, self.matrix_result]:
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #1e1e2e;
                    color: #cdd6f4;
                    gridline-color: #45475a;
                }
                QHeaderView::section {
                    background-color: #313244;
                    color: #cdd6f4;
                    padding: 5px;
                    border: none;
                }
                QTableWidget::item {
                    padding: 5px;
                }
                QTableWidget::item:selected {
                    background-color: #45475a;
                }
            """)
        
        # Ajout des matrices au layout
        matrix_area.addWidget(a_group)
        matrix_area.addWidget(b_group)
        matrix_area.addWidget(result_group)
        
        # Zone de démonstration
        demo_group = QGroupBox("Démonstration")
        demo_layout = QVBoxLayout()
        
        self.matrix_demo = QTextEdit()
        self.matrix_demo.setReadOnly(True)
        self.matrix_demo.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 5px;
                font-family: monospace;
            }
        """)
        
        demo_layout.addWidget(self.matrix_demo)
        demo_group.setLayout(demo_layout)
        
        # Ajout au layout principal
        layout.addLayout(matrix_controls)
        layout.addLayout(matrix_area)
        layout.addWidget(demo_group)
        
        # Initialisation des matrices
        self.init_matrices()
        
        # Ajout de l'onglet
        self.tabs.addTab(tab, "Matrices")
    
    def setup_factorization_tab(self):
        """Configure l'onglet de factorisation"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Zone de saisie
        input_group = QGroupBox("Expression à factoriser")
        input_layout = QHBoxLayout()
        
        self.factor_input = QLineEdit()
        self.factor_input.setPlaceholderText("Ex: x^2 - 4, x^3 + 2x^2 - 5x - 6")
        
        factor_btn = QPushButton("Factoriser")
        factor_btn.clicked.connect(self.factor_expression)
        factor_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #b4c9fc;
            }
        """)
        
        input_layout.addWidget(self.factor_input)
        input_layout.addWidget(factor_btn)
        input_group.setLayout(input_layout)
        
        # Zone de résultat
        result_group = QGroupBox("Résultat")
        result_layout = QVBoxLayout()
        
        self.factor_result = QTextEdit()
        self.factor_result.setReadOnly(True)
        self.factor_result.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #a6e3a1;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 10px;
                font-family: monospace;
                font-size: 14px;
            }
        """)
        
        result_layout.addWidget(self.factor_result)
        result_group.setLayout(result_layout)
        
        # Zone de démonstration
        demo_group = QGroupBox("Démonstration pas à pas")
        demo_layout = QVBoxLayout()
        
        self.factor_demo = QTextEdit()
        self.factor_demo.setReadOnly(True)
        self.factor_demo.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 10px;
                font-family: monospace;
            }
        """)
        
        demo_layout.addWidget(self.factor_demo)
        demo_group.setLayout(demo_layout)
        
        # Exemples
        examples_group = QGroupBox("Exemples")
        examples_layout = QHBoxLayout()
        
        examples = [
            "x² - 4",
            "x³ - 6x² + 11x - 6",
            "x⁴ - 16",
            "2x² + 5x - 3"
        ]
        
        for example in examples:
            btn = QPushButton(example)
            btn.clicked.connect(lambda _, e=example: self.factor_input.setText(e))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #313244;
                    color: #cdd6f4;
                    border: 1px solid #45475a;
                    border-radius: 3px;
                    padding: 5px 10px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #45475a;
                }
            """)
            examples_layout.addWidget(btn)
        
        examples_group.setLayout(examples_layout)
        
        # Ajout au layout principal
        layout.addWidget(input_group)
        layout.addWidget(result_group)
        layout.addWidget(demo_group)
        layout.addWidget(examples_group)
        
        # Ajout de l'onglet
        self.tabs.addTab(tab, "Factorisation")
    
    # Méthodes pour les graphiques
    def plot_function(self):
        """Trace la fonction saisie"""
        try:
            expr = self.function_input.text().strip()
            if not expr:
                return
                
            # Nettoyer l'expression
            expr = expr.replace('^', '**').replace(' ', '')
            
            # Créer un tableau de valeurs x
            x = np.linspace(
                self.x_min.value(), 
                self.x_max.value(), 
                1000
            )
            
            # Évaluer l'expression
            y = eval(expr, {
                'x': x,
                'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                'pi': np.pi, 'e': np.e
            })
            
            # Tracer la fonction
            self.canvas.axes.clear()
            self.canvas.axes.plot(x, y, label=f"${self.format_math_expr(expr)}$")
            
            # Mise en forme
            self.canvas.axes.set_xlabel('x')
            self.canvas.axes.set_ylabel('f(x)')
            self.canvas.axes.set_title(f'Fonction: ${self.format_math_expr(expr)}$')
            
            if self.show_grid.isChecked():
                self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
                
            if self.show_legend.isChecked():
                self.canvas.axes.legend()
            
            # Mise à jour du canvas
            self.canvas.draw()
            
            # Mise à jour de la démonstration
            self.update_demo(expr)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du tracé: {str(e)}")
    
    def export_plot(self):
        """Exporte le graphique dans un fichier"""
        if not hasattr(self, 'canvas') or not self.canvas.fig.axes:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le graphique",
            "",
            "Images (*.png *.jpg *.pdf);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                self.canvas.fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='#1e1e2e')
                QMessageBox.information(self, "Succès", "Le graphique a été exporté avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export: {str(e)}")
    
    def update_demo(self, expr):
        """Met à jour la démonstration pour le graphique"""
        try:
            x = sp.symbols('x')
            expr_sympy = sp.sympify(expr.replace('^', '**'))
            
            # Calculer la dérivée
            derivative = sp.diff(expr_sympy, x)
            
            # Calculer les racines
            roots = sp.solve(expr_sympy, x)
            
            # Calculer les points critiques
            critical_points = sp.solve(derivative, x)
            
            # Préparer le texte de démonstration
            demo_text = f"""Analyse de la fonction f(x) = {sp.latex(expr_sympy)}

Dérivée: f'(x) = {sp.latex(derivative)}

Racines (f(x) = 0):
"""
            if roots:
                for i, root in enumerate(roots, 1):
                    demo_text += f"x{i} = {sp.latex(root)}\n"
            else:
                demo_text += "Aucune racine réelle\n"
                
            demo_text += "\nPoints critiques (f'(x) = 0):\n"
            if critical_points:
                for i, point in enumerate(critical_points, 1):
                    demo_text += f"x{i} = {sp.latex(point)}\n"
            else:
                demo_text += "Aucun point critique\n"
            
            self.demo_text.setPlainText(demo_text)
            
        except Exception as e:
            self.demo_text.setPlainText(f"Erreur lors de l'analyse de la fonction: {str(e)}")
    
    def format_math_expr(self, expr):
        """Formate une expression mathématique pour l'affichage"""
        return expr.replace('**', '^').replace('*', '·')
    
    # Méthodes pour les matrices
    def init_matrices(self):
        """Initialise les tableaux de matrices"""
        self.update_matrix_size()
    
    def update_matrix_size(self):
        """Met à jour la taille des matrices"""
        rows = self.matrix_rows.value()
        cols = self.matrix_cols.value()
        
        for matrix in [self.matrix_a, self.matrix_b]:
            matrix.setRowCount(rows)
            matrix.setColumnCount(cols)
            
            # Remplir avec des zéros
            for i in range(rows):
                for j in range(cols):
                    # Vérifier si l'item existe déjà
                    if matrix.item(i, j) is None:
                        item = QTableWidgetItem("0")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        matrix.setItem(i, j, item)
        
        # Mettre à jour la matrice résultat
        self.matrix_result.setRowCount(rows)
        self.matrix_result.setColumnCount(cols)
    
    def get_matrix_from_table(self, table):
        """Récupère une matrice depuis un QTableWidget"""
        try:
            rows = table.rowCount()
            cols = table.columnCount()
            matrix = np.zeros((rows, cols))
            
            for i in range(rows):
                for j in range(cols):
                    item = table.item(i, j)
                    if item is not None and item.text().strip():
                        try:
                            matrix[i, j] = float(item.text())
                        except ValueError:
                            QMessageBox.warning(self, "Erreur", f"Valeur invalide en position ({i+1}, {j+1})")
                            return None
            
            return matrix
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la lecture de la matrice: {str(e)}")
            return None
    
    def set_matrix_to_table(self, matrix, table):
        """Affiche une matrice dans un QTableWidget"""
        try:
            if matrix is None or not isinstance(matrix, np.ndarray):
                return
                
            rows, cols = matrix.shape
            table.setRowCount(rows)
            table.setColumnCount(cols)
            
            for i in range(rows):
                for j in range(cols):
                    try:
                        # Formater le nombre avec 2 décimales
                        value = float(matrix[i, j])
                        item = QTableWidgetItem(f"{value:.2f}")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        table.setItem(i, j, item)
                    except (ValueError, TypeError) as e:
                        # En cas d'erreur, afficher une cellule vide
                        item = QTableWidgetItem("")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        table.setItem(i, j, item)
                        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage de la matrice: {str(e)}")
    
    # Méthodes pour la factorisation
    def factor_expression(self):
        """Factorise l'expression saisie"""
        try:
            expr = self.factor_input.text().strip()
            if not expr:
                return
                
            # Nettoyer l'expression
            expr = expr.replace('^', '**').replace(' ', '')
            
            # Convertir en expression sympy
            x = sp.symbols('x')
            try:
                expr_sympy = sp.sympify(expr)
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Expression invalide: {str(e)}")
                return
            
            # Factoriser
            factored = sp.factor(expr_sympy)
            
            # Afficher le résultat
            self.factor_result.setPlainText(f"{sp.latex(expr_sympy)} = {sp.latex(factored)}")
            
            # Mettre à jour la démonstration
            self.update_factorization_demo(expr_sympy, factored)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la factorisation: {str(e)}")
    
    def update_factorization_demo(self, expr, factored):
        """Met à jour la démonstration pour la factorisation"""
        try:
            # Définir le symbole x au début de la méthode
            x = sp.Symbol('x')
            
            demo_text = f"Étapes de factorisation pour {sp.latex(expr)}:\n\n"
            
            # Si l'expression est déjà factorisée
            if expr == factored:
                demo_text += "L'expression est déjà sous sa forme factorisée.\n"
            else:
                # Afficher les étapes intermédiaires
                demo_text += "1. Expression originale: " + sp.latex(expr) + "\n"
                
                # Si c'est une différence de carrés
                if expr.is_Add and len(expr.args) == 2:
                    a_sq = None
                    b_sq = None
                    
                    for term in expr.args:
                        if term.is_Pow and term.args[1] == 2:
                            if a_sq is None:
                                a_sq = term.args[0]
                            else:
                                b_sq = term.args[0]
                    
                    if a_sq is not None and b_sq is not None:
                        demo_text += f"2. Reconnaissance d'une différence de carrés: {sp.latex(a_sq**2 - b_sq**2)}\n"
                        demo_text += f"3. Application de l'identité remarquable: a² - b² = (a - b)(a + b)\n"
                        demo_text += f"4. Résultat: {sp.latex(factored)}\n"
                
                # Si c'est un trinôme du second degré
                elif expr.is_Polynomial and sp.degree(expr) == 2:
                    a, b, c = sp.Poly(expr, x).all_coeffs()
                    delta = b**2 - 4*a*c
                    
                    demo_text += f"2. Calcul du discriminant: Δ = b² - 4ac = {b}² - 4·{a}·{c} = {delta}\n"
                    
                    if delta > 0:
                        x1 = (-b + sp.sqrt(delta)) / (2*a)
                        x2 = (-b - sp.sqrt(delta)) / (2*a)
                        demo_text += f"3. Racines réelles: x1 = {sp.latex(x1)}, x2 = {sp.latex(x2)}\n"
                        demo_text += f"4. Forme factorisée: {a}(x - ({sp.latex(x1)}))(x - ({sp.latex(x2)}))\n"
                    elif delta == 0:
                        x0 = -b / (2*a)
                        demo_text += f"3. Racine double: x0 = {sp.latex(x0)}\n"
                        demo_text += f"4. Forme factorisée: {a}(x - ({sp.latex(x0)}))²\n"
                    else:
                        demo_text += "3. Pas de racines réelles (Δ < 0)\n"
                        demo_text += "4. La factorisation dans ℝ n'est pas possible\n"
                
                # Autres cas
                else:
                    demo_text += "2. Recherche de facteurs communs...\n"
                    demo_text += "3. Application des identités remarquables...\n"
                    demo_text += f"4. Forme factorisée: {sp.latex(factored)}\n"
                demo_text += f"\nVérification du résultat:\n"
                # Vérification du résultat
                expanded = sp.expand(factored)
                if sp.simplify(expr - expanded) == 0:
                    demo_text += f"✓ Vérification réussie: {sp.latex(expr)} = {sp.latex(expanded)}"
                else:
                    demo_text += f"❌ Erreur: {sp.latex(expr)} ≠ {sp.latex(expanded)}"
            
            self.factor_demo.setPlainText(demo_text)
            
        except Exception as e:
            self.factor_demo.setPlainText(f"Erreur lors de la démonstration: {str(e)}")
