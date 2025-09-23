# SmartCalc Web - Calculatrice en Ligne

Une version web de SmartCalc, déployée sur Vercel. Cette calculatrice scientifique offre des fonctionnalités avancées de calcul et de conversion d'unités.

## 🚀 Fonctionnalités

- **Calculatrice Standard** : Opérations arithmétiques de base
- **Calculatrice Scientifique** : Fonctions trigonométriques, logarithmiques, exponentielles
- **Convertisseur d'Unités** : Conversion entre différentes unités de mesure
- **Historique** : Sauvegarde automatique des calculs
- **Interface Responsive** : Compatible mobile et desktop
- **Mode Sombre** : Interface optimisée pour le confort visuel

## 📱 Utilisation

### Calculatrice Standard
- Saisie directe des nombres et opérateurs
- Support des opérations : `+`, `-`, `×`, `÷`
- Fonctions : pourcentage, changement de signe
- Raccourcis clavier disponibles

### Calculatrice Scientifique
- Fonctions trigonométriques : `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Fonctions logarithmiques : `log`, `ln`, `exp`
- Constantes : `pi`, `e`
- Modes d'angle : Degrés, Radians, Gradians
- Expressions mathématiques complexes

### Convertisseur d'Unités
- **Longueur** : mètres, kilomètres, centimètres, pouces, pieds, etc.
- **Masse** : kilogrammes, grammes, livres, onces, etc.
- **Température** : Celsius, Fahrenheit, Kelvin
- **Volume** : litres, millilitres, gallons, etc.
- **Temps** : secondes, minutes, heures, jours, etc.

## 🔧 Développement Local

### Prérequis
- Python 3.8+
- pip

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/mackly45/SmartCalc.git
cd SmartCalc

# Installer les dépendances web
pip install -r requirements-web.txt

# Lancer l'application
python app.py
```

L'application sera accessible à `http://localhost:5000`

### Structure du Projet

```
SmartCalc/
├── app.py                 # Application Flask principale
├── models/               # Modèles de calcul
│   ├── calculator_model.py
│   ├── scientific_model.py
│   └── conversion_model.py
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── scientific.html
│   └── converter.html
├── static/              # Ressources statiques
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── calculator.js
│       ├── scientific.js
│       └── converter.js
├── vercel.json          # Configuration Vercel
└── requirements-web.txt # Dépendances web
```

## 🚀 Déploiement sur Vercel

### Méthode 1: Interface Vercel
1. Créer un compte sur [Vercel](https://vercel.com)
2. Connecter votre dépôt GitHub
3. Importer le projet
4. Vercel détectera automatiquement la configuration

### Méthode 2: CLI Vercel
```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer
vercel --prod
```

### Variables d'Environnement
Aucune variable d'environnement spéciale n'est requise pour le déploiement de base.

## 📚 API Endpoints

### Calculatrice Standard
- `POST /api/calculate` - Effectuer des calculs de base

### Calculatrice Scientifique
- `POST /api/scientific/calculate` - Évaluer des expressions mathématiques
- `POST /api/scientific/function` - Fonctions spéciales
- `POST /api/scientific/angle-mode` - Changer le mode d'angle

### Convertisseur
- `POST /api/convert` - Convertir entre unités
- `GET /api/convert/units/{category}` - Obtenir les unités d'une catégorie

### Utilitaires
- `GET /health` - Vérification de santé
- `POST /api/history/clear` - Effacer l'historique

## 🎨 Personnalisation

### Thèmes
L'application utilise un thème sombre par défaut. Pour personnaliser :
- Modifier `static/css/style.css`
- Ajuster les variables CSS dans `:root`

### Ajout de Fonctionnalités
1. Créer de nouveaux modèles dans `models/`
2. Ajouter les routes dans `app.py`
3. Créer les templates correspondants
4. Implémenter la logique JavaScript

## 🔍 Raccourcis Clavier

### Calculatrice Standard
- `0-9` : Saisie des chiffres
- `+`, `-`, `*`, `/` : Opérateurs
- `Enter` ou `=` : Calculer
- `Escape` ou `C` : Effacer
- `Backspace` : Retour arrière

### Calculatrice Scientifique
- `Ctrl+Enter` : Calculer l'expression
- `Ctrl+L` : Effacer l'entrée
- `Ctrl+H` : Effacer l'historique
- `Ctrl+D` : Mode degrés
- `Ctrl+R` : Mode radians

## 🐛 Résolution de Problèmes

### Erreurs Communes
1. **Erreur de syntaxe** : Vérifier la syntaxe de l'expression mathématique
2. **Division par zéro** : Éviter les divisions par zéro
3. **Domaine invalide** : Vérifier le domaine des fonctions (ex: sqrt de nombre négatif)

### Debugging
- Ouvrir les outils de développement du navigateur (F12)
- Consulter la console pour les erreurs JavaScript
- Vérifier l'onglet Network pour les erreurs d'API

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commit vos changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📞 Support

- 📧 Email : support@smartcalc.dev
- 🐛 Issues : [GitHub Issues](https://github.com/mackly45/SmartCalc/issues)
- 📖 Documentation : [GitHub Wiki](https://github.com/mackly45/SmartCalc/wiki)

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile sur GitHub !