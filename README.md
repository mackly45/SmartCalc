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

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/SmartCalc.git
   cd SmartCalc
   ```

2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # OU
   .\venv\Scripts\activate  # Sur Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
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
