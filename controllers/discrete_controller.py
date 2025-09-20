from __future__ import annotations

from PyQt6.QtCore import QObject

from models.discrete_model import DiscreteModel
from views.discrete_view import DiscreteView


class DiscreteController(QObject):
    def __init__(self, model: DiscreteModel, view: DiscreteView):
        super().__init__()
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        v = self.view
        v.factorial_clicked.connect(self._on_factorial)
        v.npr_clicked.connect(self._on_npr)
        v.ncr_clicked.connect(self._on_ncr)

        v.gcd_clicked.connect(self._on_gcd)
        v.lcm_clicked.connect(self._on_lcm)
        v.isprime_clicked.connect(self._on_isprime)
        v.factors_clicked.connect(self._on_factors)
        v.powmod_clicked.connect(self._on_powmod)

        v.fib_clicked.connect(self._on_fibonacci)

    # --- Slots ---
    def _show(self, value):
        self.view.show_result(str(value))

    def _on_factorial(self, n: int):
        try:
            self._show(self.model.factorial(n))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_npr(self, n: int, r: int):
        try:
            self._show(self.model.nPr(n, r))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_ncr(self, n: int, r: int):
        try:
            self._show(self.model.nCr(n, r))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_gcd(self, a: int, b: int):
        try:
            self._show(self.model.gcd(a, b))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_lcm(self, a: int, b: int):
        try:
            self._show(self.model.lcm(a, b))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_isprime(self, a: int):
        try:
            self._show(self.model.is_prime(a))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_factors(self, a: int):
        try:
            self._show(self.model.prime_factors(a))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_powmod(self, a: int, e: int, m: int):
        try:
            self._show(self.model.pow_mod(a, e, m))
        except Exception as e:
            self.view.show_error(str(e))

    def _on_fibonacci(self, n: int):
        try:
            self._show(self.model.fibonacci(n))
        except Exception as e:
            self.view.show_error(str(e))


    def _on_powmod(self, a: int, e: int, m: int) -> None:
        try:
            result = self.model.pow_mod(a, e, m)
            self._show(result)
        except ValueError as e:
            self.view.show_error(str(e))

    def _on_fibonacci(self, n: int) -> None:
        try:
            result = self.model.fibonacci(n)
            self._show(result)
        except ValueError as e:
            self.view.show_error(str(e))
