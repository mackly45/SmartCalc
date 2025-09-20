from __future__ import annotations
from math import gcd as _gcd
from typing import Dict


class DiscreteModel:
    """
    Modèle pour les opérations de mathématiques discrètes.
    Implémente les opérations de base de la théorie des nombres et de la combinatoire.
    """

    def factorial(self, n: int) -> int:
        """Retourne la factorielle de n (n!)."""
        if n < 0:
            raise ValueError(
                "La factorielle n'est définie que pour les entiers positifs"
            )
        if n == 0 or n == 1:
            return 1
        return n * self.factorial(n - 1)

    def arrangement(self, n: int, k: int) -> int:
        """Retourne le nombre d'arrangements de k éléments parmi n."""
        if n < 0 or k < 0:
            raise ValueError("Les valeurs doivent être positives")
        if k > n:
            return 0
        return self.factorial(n) // self.factorial(n - k)

    def combination(self, n: int, k: int) -> int:
        """Retourne le nombre de combinaisons de k éléments parmi n."""
        if n < 0 or k < 0:
            raise ValueError("Les valeurs doivent être positives")
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        return self.arrangement(n, k) // self.factorial(k)

    def gcd(self, a: int, b: int) -> int:
        """Retourne le plus grand commun diviseur de a et b."""
        return _gcd(a, b) if a or b else 0

    def lcm(self, a: int, b: int) -> int:
        """Retourne le plus petit commun multiple de a et b."""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // self.gcd(a, b)

    def is_prime(self, n: int) -> bool:
        """Vérifie si un nombre est premier."""
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        i = 5
        w = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += w
            w = 6 - w
        return True

    def prime_factors(self, n: int) -> Dict[int, int]:
        """
        Retourne les facteurs premiers d'un nombre sous forme de dictionnaire
        {facteur: exposant, ...}
        """
        if n == 0:
            raise ValueError("0 n'a pas de facteurs premiers")
        if n == 1:
            return {1: 1}

        factors: Dict[int, int] = {}

        # Traitement des facteurs 2
        count = 0
        while n % 2 == 0:
            count += 1
            n = n // 2
        if count > 0:
            factors[2] = count

        # Vérification des nombres impairs jusqu'à sqrt(n)
        i = 3
        while i * i <= n:
            count = 0
            while n % i == 0:
                count += 1
                n = n // i
            if count > 0:
                factors[i] = count
            i += 2

        # Si n est un nombre premier > 2
        if n > 2:
            factors[n] = 1

        return factors

    def pow_mod(self, base: int, exponent: int, modulus: int) -> int:
        """Calcule (base^exponent) % modulus de manière efficace."""
        if modulus <= 0:
            raise ValueError("Le module doit être strictement positif")
        if exponent < 0:
            raise ValueError("L'exposant doit être positif")

        result = 1
        base = base % modulus

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus

        return result

    def fibonacci(self, n: int) -> int:
        """Retourne le n-ième nombre de Fibonacci."""
        if n < 0:
            raise ValueError("L'indice doit être positif")
        if n == 0:
            return 0
        if n == 1:
            return 1

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
