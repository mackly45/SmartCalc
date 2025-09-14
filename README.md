# SmartCalc - Calculatrice Scientifique

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
