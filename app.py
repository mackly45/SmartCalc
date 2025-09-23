#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import os
import sys
import math

# Ajouter le répertoire courant au PATH pour importer les modèles
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.calculator_model import CalculatorModel
from models.scientific_model import ScientificModel
from models.conversion_model import ConversionModel

app = Flask(__name__)

# Instances des modèles
calculator_model = CalculatorModel()
scientific_model = ScientificModel()
conversion_model = ConversionModel()

@app.route('/')
def index():
    """Page d'accueil avec la calculatrice de base"""
    return render_template('index.html')

@app.route('/scientific')
def scientific():
    """Page de la calculatrice scientifique"""
    return render_template('scientific.html')

@app.route('/converter')
def converter():
    """Page du convertisseur d'unités"""
    categories = conversion_model.get_categories()
    return render_template('converter.html', categories=categories)

# === API Routes pour la calculatrice de base ===

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API pour les calculs de base"""
    try:
        data = request.get_json()
        action = data.get('action')
        value = data.get('value', '')
        
        if action == 'clear':
            calculator_model.clear()
        elif action == 'number':
            calculator_model.append_number(value)
        elif action == 'operator':
            calculator_model.add_operator(value)
        elif action == 'equals':
            calculator_model.calculate()
        elif action == 'decimal':
            calculator_model.add_decimal()
        elif action == 'percentage':
            calculator_model.percentage()
        elif action == 'toggle_sign':
            calculator_model.toggle_sign()
        
        return jsonify({
            'success': True,
            'current_value': calculator_model.current_value,
            'expression': calculator_model.expression
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# === API Routes pour la calculatrice scientifique ===

@app.route('/api/scientific/calculate', methods=['POST'])
def api_scientific_calculate():
    """API pour les calculs scientifiques"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        variables = data.get('variables', {})
        
        result = scientific_model.evaluate_expression(expression, variables)
        
        return jsonify({
            'success': True,
            'result': result,
            'history': scientific_model.get_history()[-10:]  # Derniers 10 calculs
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/scientific/function', methods=['POST'])
def api_scientific_function():
    """API pour les fonctions scientifiques spéciales"""
    try:
        data = request.get_json()
        function = data.get('function')
        value = data.get('value')
        
        result = None
        
        if function == 'factorial':
            result = scientific_model.factorial(int(value))
        elif function == 'sin':
            result = scientific_model._wrap_angle_math(math.sin)(float(value))
        elif function == 'cos':
            result = scientific_model._wrap_angle_math(math.cos)(float(value))
        elif function == 'tan':
            result = scientific_model._wrap_angle_math(math.tan)(float(value))
        elif function == 'sqrt':
            result = math.sqrt(float(value))
        elif function == 'log':
            result = math.log10(float(value))
        elif function == 'ln':
            result = math.log(float(value))
        elif function == 'exp':
            result = math.exp(float(value))
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/scientific/angle-mode', methods=['POST'])
def api_set_angle_mode():
    """API pour changer le mode d'angle"""
    try:
        data = request.get_json()
        mode = data.get('mode', 'DEG')
        
        scientific_model.set_angle_mode(mode)
        
        return jsonify({
            'success': True,
            'mode': scientific_model.angle_mode
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# === API Routes pour le convertisseur ===

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API pour les conversions d'unités"""
    try:
        data = request.get_json()
        value = float(data.get('value', 0))
        from_unit = data.get('from_unit')
        to_unit = data.get('to_unit')
        category = data.get('category')
        
        result = conversion_model.convert(value, from_unit, to_unit, category)
        
        return jsonify({
            'success': True,
            'result': result,
            'history': conversion_model.get_conversion_history()[-5:]  # Dernières 5 conversions
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/convert/units/<category>')
def api_get_units(category):
    """API pour obtenir les unités d'une catégorie"""
    try:
        units = conversion_model.get_units_for_category(category)
        return jsonify({
            'success': True,
            'units': units
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# === API Routes pour l'historique ===

@app.route('/api/history/clear', methods=['POST'])
def api_clear_history():
    """API pour effacer l'historique"""
    try:
        data = request.get_json()
        model_type = data.get('type', 'scientific')
        
        if model_type == 'scientific':
            scientific_model.clear_history()
        elif model_type == 'conversion':
            conversion_model.clear_history()
        
        return jsonify({
            'success': True,
            'message': 'Historique effacé'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# === Route pour servir les ressources statiques ===

@app.route('/health')
def health_check():
    """Point de santé pour Vercel"""
    return jsonify({
        'status': 'healthy',
        'message': 'SmartCalc API is running'
    })

if __name__ == '__main__':
    # Configuration pour le développement local
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))