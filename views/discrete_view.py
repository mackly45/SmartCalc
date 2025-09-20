from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QGroupBox,
)
from PyQt6.QtCore import Qt, pyqtSignal


class DiscreteView(QWidget):
    """
    Vue pour les mathématiques discrètes.
    Sections: Combinatoire, Arithmétique, Suites.
    """

    # Signaux combinatoire
    factorial_clicked = pyqtSignal(int)
    npr_clicked = pyqtSignal(int, int)
    ncr_clicked = pyqtSignal(int, int)

    # Signaux arithmétique
    gcd_clicked = pyqtSignal(int, int)
    lcm_clicked = pyqtSignal(int, int)
    isprime_clicked = pyqtSignal(int)
    factors_clicked = pyqtSignal(int)
    powmod_clicked = pyqtSignal(int, int, int)

    # Signaux suites
    fib_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Mathématiques Discrètes")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Zone de résultat globale
        self.result_label = QLabel("Prêt")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # --- Combinatoire ---
        combo_group = QGroupBox("Combinatoire")
        combo_layout = QGridLayout()

        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("n")
        self.r_input = QLineEdit()
        self.r_input.setPlaceholderText("r")

        btn_fact = QPushButton("n!")
        btn_npr = QPushButton("nPr")
        btn_ncr = QPushButton("nCr")

        btn_fact.clicked.connect(self._emit_factorial)
        btn_npr.clicked.connect(self._emit_npr)
        btn_ncr.clicked.connect(self._emit_ncr)

        combo_layout.addWidget(QLabel("n:"), 0, 0)
        combo_layout.addWidget(self.n_input, 0, 1)
        combo_layout.addWidget(QLabel("r:"), 0, 2)
        combo_layout.addWidget(self.r_input, 0, 3)
        combo_layout.addWidget(btn_fact, 1, 0)
        combo_layout.addWidget(btn_npr, 1, 1)
        combo_layout.addWidget(btn_ncr, 1, 2)
        combo_group.setLayout(combo_layout)

        # --- Arithmétique ---
        arith_group = QGroupBox("Arithmétique / Nombres")
        arith_layout = QGridLayout()

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("a")
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("b")
        self.m_input = QLineEdit()
        self.m_input.setPlaceholderText("m (mod)")

        btn_gcd = QPushButton("pgcd(a,b)")
        btn_lcm = QPushButton("ppcm(a,b)")
        btn_prime = QPushButton("est premier ?")
        btn_factors = QPushButton("facteurs(a)")
        btn_powmod = QPushButton("pow_mod(a^e mod m)")

        btn_gcd.clicked.connect(self._emit_gcd)
        btn_lcm.clicked.connect(self._emit_lcm)
        btn_prime.clicked.connect(self._emit_isprime)
        btn_factors.clicked.connect(self._emit_factors)
        btn_powmod.clicked.connect(self._emit_powmod)

        arith_layout.addWidget(QLabel("a:"), 0, 0)
        arith_layout.addWidget(self.a_input, 0, 1)
        arith_layout.addWidget(QLabel("b/e:"), 0, 2)
        arith_layout.addWidget(self.b_input, 0, 3)
        arith_layout.addWidget(QLabel("m:"), 0, 4)
        arith_layout.addWidget(self.m_input, 0, 5)
        arith_layout.addWidget(btn_gcd, 1, 0)
        arith_layout.addWidget(btn_lcm, 1, 1)
        arith_layout.addWidget(btn_prime, 1, 2)
        arith_layout.addWidget(btn_factors, 1, 3)
        arith_layout.addWidget(btn_powmod, 1, 4)
        arith_group.setLayout(arith_layout)

        # --- Suites ---
        seq_group = QGroupBox("Suites")
        seq_layout = QHBoxLayout()
        self.fib_input = QLineEdit()
        self.fib_input.setPlaceholderText("n (Fibonacci)")
        btn_fib = QPushButton("Fibonacci(n)")
        btn_fib.clicked.connect(self._emit_fib)
        seq_layout.addWidget(self.fib_input)
        seq_layout.addWidget(btn_fib)
        seq_group.setLayout(seq_layout)

        # Assembler
        layout.addWidget(combo_group)
        layout.addWidget(arith_group)
        layout.addWidget(seq_group)
        layout.addWidget(self.result_label)
        layout.addStretch()

    # --- Helpers d'émission ---
    def _to_int(self, widget: QLineEdit) -> int:
        """Convertit le texte d'un QLineEdit en entier."""
        text = widget.text().strip()
        if not text:
            raise ValueError("Veuillez entrer une valeur")
        try:
            return int(text)
        except ValueError as e:
            raise ValueError("Veuillez entrer un nombre entier valide") from e

    def _emit_factorial(self):
        try:
            n = self._to_int(self.n_input)
            self.factorial_clicked.emit(n)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_npr(self):
        try:
            n = self._to_int(self.n_input)
            r = self._to_int(self.r_input)
            self.npr_clicked.emit(n, r)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_ncr(self):
        try:
            n = self._to_int(self.n_input)
            r = self._to_int(self.r_input)
            self.ncr_clicked.emit(n, r)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_gcd(self):
        try:
            a = self._to_int(self.a_input)
            b = self._to_int(self.b_input)
            self.gcd_clicked.emit(a, b)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_lcm(self):
        try:
            a = self._to_int(self.a_input)
            b = self._to_int(self.b_input)
            self.lcm_clicked.emit(a, b)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_isprime(self):
        try:
            a = self._to_int(self.a_input)
            self.isprime_clicked.emit(a)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_factors(self):
        try:
            a = self._to_int(self.a_input)
            self.factors_clicked.emit(a)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_powmod(self):
        try:
            a = self._to_int(self.a_input)
            e = self._to_int(self.b_input)
            m = self._to_int(self.m_input)
            self.powmod_clicked.emit(a, e, m)
        except ValueError as e:
            self.show_error(str(e))

    def _emit_fib(self):
        try:
            n = self._to_int(self.fib_input)
            self.fib_clicked.emit(n)
        except ValueError as e:
            self.show_error(str(e))

    # --- Slots d'affichage ---
    def show_result(self, text: str) -> None:
        """Affiche un résultat dans la vue."""
        self.result_label.setText(str(text))
        self.result_label.setStyleSheet("")

    def show_error(self, message: str) -> None:
        """Affiche un message d'erreur dans la vue."""
        self.result_label.setText(f"Erreur: {message}")
        self.result_label.setStyleSheet("color: #f38ba8;")
