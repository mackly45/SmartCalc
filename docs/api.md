# Documentation de l'API

## Modèle de la Calculatrice

### `CalculatorModel`

Classe principale gérant la logique de la calculatrice.

#### Méthodes

##### `__init__()`
Initialise une nouvelle instance de la calculatrice.

##### `clear()`
Réinitialise la calculatrice à son état initial.

##### `append_number(number: str) -> None`
Ajoute un chiffre ou un point décimal à la valeur actuelle.

**Paramètres :**
- `number` (str) : Le chiffre ou le point à ajouter

##### `add_operator(operator: str) -> None`
Ajoute un opérateur à l'expression en cours.

**Paramètres :**
- `operator` (str) : L'opérateur à ajouter (+, -, ×, ÷, etc.)

##### `calculate() -> None`
Évalue l'expression en cours et met à jour le résultat.

##### `add_decimal() -> None`
Ajoute un point décimal à la valeur actuelle.

##### `percentage() -> None`
Calcule le pourcentage de la valeur actuelle.

##### `toggle_sign() -> None`
Change le signe de la valeur actuelle.

## Modèle Scientifique

### `ScientificCalculatorModel`

Classe étendant les fonctionnalités de base avec des opérations scientifiques.

#### Méthodes

##### `evaluate_expression(expression: str) -> float`
Évalue une expression mathématique avancée.

**Paramètres :**
- `expression` (str) : L'expression à évaluer

**Retourne :**
- float : Le résultat du calcul

## Constantes

- `VERSION` : Version actuelle de l'application
- `AUTHOR` : Auteur du projet
- `LICENSE` : Type de licence

## Exemples d'Utilisation

```python
from smartcalc.models import CalculatorModel, ScientificCalculatorModel

# Création d'une instance
calc = CalculatorModel()

# Calcul simple
calc.append_number("5")
calc.add_operator("+")
calc.append_number("3")
calc.calculate()
print(calc.current_value)  # Affiche 8

# Calcul scientifique
sci = ScientificCalculatorModel()
result = sci.evaluate_expression("sin(45) + cos(45)")
print(result)  # Affiche 1.4142
```

## Codes d'Erreur

| Code | Description |
|------|-------------|
| 1 | Erreur de syntaxe dans l'expression |
| 2 | Division par zéro |
| 3 | Valeur non définie |
| 4 | Dépassement de capacité |

## Sécurité

Toutes les entrées utilisateur sont validées pour prévenir les injections de code. L'évaluation des expressions utilise un analyseur syntaxique sûr qui n'exécute pas de code arbitraire.
