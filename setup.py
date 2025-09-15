"""Configuration du package pour l'installation via pip.

Ce module configure les métadonnées et les dépendances du package SmartCalc.
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    import sys

    print(
        "Erreur: setuptools n'est pas installé. Veuillez l'installer avec 'pip install setuptools'",
        file=sys.stderr,
    )
    sys.exit(1)

# Configuration de l'installation du package
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="smartcalc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "smartcalc=smartcalc.main:main",
        ],
    },
    python_requires=">=3.8",
    author="Votre Nom",
    author_email="votre@email.com",
    description="Une calculatrice scientifique avancée",
    url="https://github.com/mackly45/SmartCalc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
