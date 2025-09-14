# SmartCalc - Calculatrice Scientifique

Une calculatrice scientifique moderne développée avec Python et PyQt6, dotée d'une interface élégante et d'animations fluides.

## Fonctionnalités

- Interface utilisateur moderne et élégante avec des animations fluides
- Écran de chargement avec logo
- Opérations arithmétiques de base (+, -, ×, ÷)
- Calculs de pourcentage
- Inversion de signe (±)
- Fonction d'effacement
- Affichage de l'expression

## Installation

1. Assurez-vous d'avoir Python 3.8 ou une version supérieure installé
2. Clonez ce dépôt
3. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

## Lancement de l'application

Pour démarrer la calculatrice, exécutez :

```bash
python main.py
```

## Structure du projet

```plaintext
SmartCalc/
├── assets/                 # Ressources graphiques
│   └── images/             # Fichiers images (logo.png doit être placé ici)
├── controllers/            # Classes contrôleurs
│   └── calculator_controller.py
├── models/                 # Modèles de données
│   └── calculator_model.py
├── views/                 # Composants d'interface
│   ├── __init__.py
│   └── calculator_view.py
├── main.py                # Point d'entrée de l'application
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

## Ajout d'images personnalisées pour les boutons

Pour ajouter des images personnalisées pour les boutons numériques (0-9) :

1. Placez vos fichiers image dans le répertoire `assets/images/`
2. Nommez-les `0.png`, `1.png`, ..., `9.png`
3. Les images seront automatiquement chargées et affichées sur les boutons correspondants

## Licence

Ce projet est open source et disponible sous licence [MIT](LICENSE).
