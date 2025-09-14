import sys
import os

try:
    import pytest
except ImportError:
    # Skip pytest decorators if pytest is not available
    import types
    sys.modules['pytest'] = types.ModuleType('pytest')
    def skip(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    sys.modules['pytest'].mark = types.SimpleNamespace()
    sys.modules['pytest'].mark.skip = skip

# Ajouter le répertoire parent au chemin Python pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Teste l'importation des modules principaux"""
    try:
        from models.calculator_model import CalculatorModel
        from models.scientific_model import ScientificCalculatorModel
        from models.currency_model import CurrencyModel
        from models.advanced_model import AdvancedCalculatorModel
        
        # Vérifier que les classes sont bien définies
        assert CalculatorModel is not None
        assert ScientificCalculatorModel is not None
        assert CurrencyModel is not None
        assert AdvancedCalculatorModel is not None
        
    except ImportError as e:
        pytest.fail(f"Erreur d'importation : {e}")

def test_basic_arithmetic():
    """Teste les opérations arithmétiques de base"""
    from models.calculator_model import CalculatorModel
    
    calc = CalculatorModel()
    
    # Test d'addition
    calc.append_number("5")  # Entrer 5
    calc.add_operator("+")   # Appuyer sur +
    calc.append_number("3")  # Entrer 3
    calc.calculate()         # Appuyer sur =
    assert calc.current_value == "8"
    
    # Test de soustraction
    calc.clear()
    calc.append_number("10")
    calc.add_operator("-")
    calc.append_number("3")
    calc.calculate()
    assert calc.current_value == "7"
    
    # Test de multiplication
    calc.clear()
    calc.append_number("5")
    calc.add_operator("×")
    calc.append_number("3")
    calc.calculate()
    assert calc.current_value == "15"
    
    # Test de division
    calc.clear()
    calc.append_number("15")
    calc.add_operator("÷")
    calc.append_number("3")
    calc.calculate()
    assert calc.current_value == "5.0"

def test_scientific_functions():
    """Teste les fonctions scientifiques de base"""
    from models.scientific_model import ScientificCalculatorModel
    
    sci = ScientificCalculatorModel()
    
    # Test de la fonction carrée
    assert sci.evaluate_expression("sqrt(16)") == 4.0
    
    # Test de la fonction puissance
    assert sci.evaluate_expression("2**3") == 8.0

# Ce test sera ignoré car il nécessite une interface graphique
@pytest.mark.skip(reason="Nécessite une interface graphique")
def test_gui_components():
    """Test des composants de l'interface graphique"""
    pass

if __name__ == "__main__":
    pytest.main(["-v", "--cov=.", "--cov-report=term-missing"])
