import sys
import os

# Ajouter le répertoire parent au chemin de recherche Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models.scientific_model import ScientificCalculatorModel
    print("Import de ScientificCalculatorModel réussi!")
    print("Classe:", ScientificCalculatorModel)
    
    # Tester la création d'une instance
    model = ScientificCalculatorModel()
    print("Instance créée avec succès:", model)
    
except ImportError as e:
    print("Erreur d'importation:", e)
    print("Chemin de recherche Python:", sys.path)
    
    # Vérifier si le fichier existe
    scientific_model_path = os.path.join(os.path.dirname(__file__), 'models', 'scientific_model.py')
    print("Chemin du fichier:", scientific_model_path)
    print("Le fichier existe:", os.path.exists(scientific_model_path))
