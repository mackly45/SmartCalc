# Installation

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation via pip

La méthode la plus simple pour installer SmartCalc est d'utiliser pip :

```bash
pip install git+https://github.com/mackly45/SmartCalc.git
```

## Installation à partir des sources

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/mackly45/SmartCalc.git
   cd SmartCalc
   ```

2. Créez et activez un environnement virtuel (recommandé) :
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

## Développement

Pour contribuer au projet, installez les dépendances de développement :

```bash
pip install -r requirements-dev.txt
```

## Vérification de l'installation

Pour vérifier que tout est correctement installé, exécutez :

```bash
python -m smartcalc --version
```

## Mise à jour

Pour mettre à jour vers la dernière version :

```bash
pip install --upgrade git+https://github.com/mackly45/SmartCalc.git
```

## Désinstallation

Pour désinstaller SmartCalc :

```bash
pip uninstall smartcalc
```
