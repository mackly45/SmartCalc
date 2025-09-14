from setuptools import setup, find_packages

setup(
    name="smartcalc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.0.0',
        'PyQt6-Qt6>=6.4.0',
        'PyQt6-sip>=13.4.0',
        'numpy>=1.20.0',
        'matplotlib>=3.4.0',
        'sympy>=1.8',
        'requests>=2.25.1',
    ],
    python_requires='>=3.8',
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Une calculatrice scientifique avancée avec interface graphique",
    url="https://github.com/votre-utilisateur/SmartCalc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'smartcalc=smartcalc.main:main',
        ],
    },
)
