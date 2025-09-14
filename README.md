# SmartCalc

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/mackly45/SmartCalc/actions/workflows/python-app.yml/badge.svg)](https://github.com/mackly45/SmartCalc/actions)
[![Documentation Status](https://github.com/mackly45/SmartCalc/actions/workflows/python-docs.yml/badge.svg)](https://mackly45.github.io/SmartCalc/)
[![Code Coverage](https://codecov.io/gh/mackly45/SmartCalc/branch/main/graph/badge.svg?token=YOUR-TOKEN-HERE)](https://codecov.io/gh/mackly45/SmartCalc)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![CodeFactor](https://www.codefactor.io/repository/github/mackly45/smartcalc/badge)](https://www.codefactor.io/repository/github/mackly45/smartcalc)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/mackly45/SmartCalc/badge)](https://api.securityscorecards.dev/projects/github.com/mackly45/SmartCalc)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=mackly45/SmartCalc)](https://dependabot.com)
[![Maintainability](https://api.codeclimate.com/v1/badges/YOUR-BADGE-ID/maintainability)](https://codeclimate.com/github/mackly45/SmartCalc/maintainability)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmackly45%2FSmartCalc.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmackly45%2FSmartCalc?ref=badge_shield)

Une calculatrice scientifique avancée développée avec Python et PyQt6, offrant des fonctionnalités de calcul scientifique, de conversion de devises et d'analyse mathématique avancée.

## Fonctionnalités

- **Calculatrice standard** : Opérations mathématiques de base
- **Calculatrice scientifique** : Fonctions trigonométriques, logarithmiques, etc.
- **Convertisseur de devises** : Mise à jour automatique des taux de change
- **Outils avancés** : 
  - Tracé de fonctions mathématiques
  - Calculs matriciels
  - Factorisation d'expressions algébriques
  - Analyse de fonctions

## Captures d'écran

![Interface de SmartCalc](docs/img/screenshot.png)

## Prérequis

- Python 3.8 ou supérieur
- Les dépendances listées dans `requirements.txt`

## Installation

### Production

1. Installation directe :
   ```bash
   pip install git+https://github.com/mackly45/SmartCalc.git
   ```

2. Ou en mode développement :
   ```bash
   git clone https://github.com/mackly45/SmartCalc.git
   cd SmartCalc
   
   # Création d'un environnement virtuel (recommandé)
   python -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # OU
   .\venv\Scripts\activate  # Sur Windows
   
   # Installation en mode développement
   pip install -e .
   ```

### Développement

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/mackly45/SmartCalc.git
   cd SmartCalc
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # OU
   .\venv\Scripts\activate  # Sur Windows
   ```

3. Installez les dépendances de développement :
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Pour exécuter les tests :
   ```bash
   pytest -v
   ```

5. Pour formater le code :
   ```bash
   black .
   ```

6. Pour vérifier la qualité du code :
   ```bash
   flake8 .
   pylint smartcalc/
   ```

## Utilisation

Lancez l'application avec :

```bash
python main.py
```

### Mode test

Pour exécuter l'application en mode test (sans interface graphique) :

```bash
python main.py --test-mode
```

## Développement

### Exécuter les tests

```bash
pytest
```

### Vérifier la qualité du code

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
