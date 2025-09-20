import os
import shutil
import PyInstaller.__main__

def main():
    print("Nettoyage des anciens builds...")
    for item in ['build', 'dist']:
        if os.path.exists(item):
            shutil.rmtree(item)
    
    print("\nConstruction de l'exécutable...")
    PyInstaller.__main__.run([
        'main.py',
        '--name=SmartCalc',
        '--onefile',
        '--windowed',
        '--noconsole',
        '--add-data=assets;assets',
        '--add-data=currency_rates.json;.',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--clean',
    ])
    
    print("\nBuild terminé ! L'exécutable se trouve dans le dossier 'dist'")

if __name__ == "__main__":
    main()
