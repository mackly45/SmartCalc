# SmartCalc - Calculatrice Scientifique

Une calculatrice scientifique moderne développée avec Python et PyQt6, dotée d'une interface élégante et de fonctionnalités avancées.

## Fonctionnalités

### Calculatrice de base
- Opérations arithmétiques (+, -, ×, ÷)
- Calculs de pourcentage (%)
- Inversion de signe (±)
- Fonction d'effacement (C)
- Affichage de l'expression

### Calculatrice Scientifique
- **Fonctions trigonométriques** : sin, cos, tan, asin, acos, atan
- **Fonctions hyperboliques** : sinh, cosh, tanh, asinh, acosh, atanh
- **Logarithmes et exponentielles** : log, ln, exp, 10^x, e^x
- **Racines** : carrée (√), cubique
- **Constantes** : π, e, φ, γ
- **Mémoire** : M+, M-, MR, MC
- **Modes d'angle** : Degrés, Radians, Grades
- **Notation** : Standard, Scientifique, Ingénieur

### Convertisseur de devises
- Support de plus de 15 devises
- Mise à jour automatique des taux de change
- Mode hors ligne avec mise en cache
- Conversion en temps réel

## Installation

1. Assurez-vous d'avoir Python 3.8 ou une version supérieure installé
2. Clonez ce dépôt
3. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
python main.py
```

## Structure du projet

```
SmartCalc/
├── assets/                 # Ressources graphiques
│   └── images/             # Fichiers images
├── controllers/            # Contrôleurs
│   ├── calculator_controller.py
│   ├── currency_controller.py
│   └── scientific_controller.py
├── models/                 # Modèles de données
│   ├── calculator_model.py
│   ├── currency_model.py
│   └── scientific_model.py
├── views/                  # Vues
│   ├── calculator_view.py
│   ├── currency_view.py
│   ├── scientific_view.py
│   └── __init__.py
├── main.py                 # Point d'entrée
└── README.md               # Ce fichier
```

## Utilisation

### Calculatrice Scientifique
1. Sélectionnez le mode d'angle (DEG/RAD/GRAD) dans le menu déroulant
2. Utilisez les boutons ou le clavier pour entrer votre expression
3. Appuyez sur = pour évaluer l'expression

### Convertisseur de devises
1. Entrez le montant à convertir
2. Sélectionnez les devises source et cible
3. Le résultat est affiché automatiquement

## Dépendances

- Python 3.8+
- PyQt6
- requests (pour le convertisseur de devises)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
