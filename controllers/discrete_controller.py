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
        v.npr_clicked.connect(self._on_arrangement)
        v.ncr_clicked.connect(self._on_combination)

        v.gcd_clicked.connect(self._on_gcd)
        v.lcm_clicked.connect(self._on_lcm)
        v.isprime_clicked.connect(self._on_isprime)
        v.factors_clicked.connect(self._on_factors)
        v.powmod_clicked.connect(self._on_powmod)
        v.fib_clicked.connect(self._on_fibonacci)

    # --- Slots ---
    def _show(self, value):
        self.view.show_result(str(value))

    def _on_factorial(self, n: int) -> None:
        try:
            self._show(self.model.factorial(n))
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_arrangement(self, n: int, r: int) -> None:
        try:
            self._show(self.model.arrangement(n, r))
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_combination(self, n: int, r: int) -> None:
        try:
            self._show(self.model.combination(n, r))
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_gcd(self, a: int, b: int) -> None:
        try:
            self._show(self.model.gcd(a, b))
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_lcm(self, a: int, b: int) -> None:
        try:
            self._show(self.model.lcm(a, b))
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_isprime(self, a: int) -> None:
        try:
            self._show(self.model.is_prime(a))
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_factors(self, a: int) -> None:
        try:
            factors = self.model.prime_factors(a)
            factors_str = " × ".join(f"{p}^{exp}" for p, exp in factors.items())
            self.view.show_result(f"{a} = {factors_str}")
        except (ValueError, TypeError) as e:
            self.view.show_error(str(e))

    def _on_powmod(self, a: int, e: int, m: int) -> None:
        try:
            result = self.model.pow_mod(a, e, m)
            self.view.show_result(f"{a}^{e} mod {m} = {result}")
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error))

    def _on_fibonacci(self, n: int) -> None:
        try:
            result = self.model.fibonacci(n)
            self.view.show_result(f"Fibonacci({n}) = {result}")
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error))
