import math
import cmath
import re
from datetime import datetime

class ScientificCalculatorModel:
    def __init__(self):
        self.memory = 0
        self.last_ans = 0
        self.angle_mode = 'DEG'  # DEG, RAD, GRAD
        self.history = []  # Liste pour stocker l'historique des calculs
        self.max_history_size = 100  # Nombre maximum d'entrées dans l'historique
        self.settings = {
            'angle_mode': 'DEG',
            'number_format': 'normal',  # normal, sci, eng
            'precision': 10
        }
    
    def set_angle_mode(self, mode):
        """Définit le mode d'angle (DEG, RAD, GRAD)"""
        if mode.upper() in ['DEG', 'RAD', 'GRAD']:
            self.settings['angle_mode'] = mode.upper()
            return True
        return False
    
    def to_radians(self, angle):
        """Convertit un angle en radians selon le mode actuel"""
        if self.settings['angle_mode'] == 'DEG':
            return math.radians(angle)
        elif self.settings['angle_mode'] == 'GRAD':
            return angle * math.pi / 200
        return angle  # Déjà en radians
    
    def from_radians(self, angle):
        """Convertit des radians vers le mode d'angle actuel"""
        if self.settings['angle_mode'] == 'DEG':
            return math.degrees(angle)
        elif self.settings['angle_mode'] == 'GRAD':
            return angle * 200 / math.pi
        return angle  # Déjà en radians
    
    def evaluate_expression(self, expression):
        """Évalue une expression mathématique"""
        try:
            # Remplacer les constantes
            expr = expression.replace('π', 'pi').replace('e', 'math.e')
            
            # Remplacer les fonctions trigonométriques avec gestion du mode angle
            if self.settings['angle_mode'] != 'RAD':
                for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                    expr = re.sub(fr'({func})\(([^)]+)\)', 
                                fr'math.{func}(self.to_radians(\2))', 
                                expr)
            else:
                for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                    expr = expr.replace(f'{func}(', f'math.{func}(')
            
            # Remplacer les autres fonctions mathématiques
            math_funcs = ['sqrt', 'log', 'log10', 'exp', 'factorial', 'gamma', 'log2']
            for func in math_funcs:
                expr = expr.replace(f'{func}(', f'math.{func}(')
            
            # Remplacer les fonctions hyperboliques
            hyp_funcs = ['sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']
            for func in hyp_funcs:
                expr = expr.replace(f'{func}(', f'math.{func}(')
            
            # Évaluer l'expression
            result = eval(expr, {'__builtins__': None}, {
                'math': math,
                'e': math.e,
                'pi': math.pi,
                'ans': self.last_ans,
                'sqrt': math.sqrt,
                'log': math.log10,
                'ln': math.log,
                'exp': math.exp,
                'abs': abs,
                'round': round,
                'floor': math.floor,
                'ceil': math.ceil,
                'sin': math.sin if self.settings['angle_mode'] == 'RAD' else lambda x: math.sin(self.to_radians(x)),
                'cos': math.cos if self.settings['angle_mode'] == 'RAD' else lambda x: math.cos(self.to_radians(x)),
                'tan': math.tan if self.settings['angle_mode'] == 'RAD' else lambda x: math.tan(self.to_radians(x)),
                'asin': lambda x: self.from_radians(math.asin(x)) if self.settings['angle_mode'] != 'RAD' else math.asin(x),
                'acos': lambda x: self.from_radians(math.acos(x)) if self.settings['angle_mode'] != 'RAD' else math.acos(x),
                'atan': lambda x: self.from_radians(math.atan(x)) if self.settings['angle_mode'] != 'RAD' else math.atan(x),
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'asinh': math.asinh,
                'acosh': math.acosh,
                'atanh': math.atanh,
                'log10': math.log10,
                'log2': math.log2,
                'factorial': math.factorial,
                'gcd': math.gcd,
                'degrees': math.degrees,
                'radians': math.radians,
                'mod': lambda x, y: x % y,
                'comb': math.comb,
                'perm': lambda n, k: math.perm(int(n), int(k)),
                'gamma': math.gamma,
                'lgamma': math.lgamma,
                'erf': math.erf,
                'erfc': math.erfc,
                'isqrt': math.isqrt,
                'isclose': math.isclose,
                'gcd': math.gcd,
                'lcm': math.lcm,
                'j': 1j,
                'complex': complex,
                'polar': cmath.polar,
                'rect': cmath.rect,
                'phase': cmath.phase,
                'polar_to_rect': lambda r, phi: (r * cmath.cos(phi), r * cmath.sin(phi)),
                'rect_to_polar': lambda x, y: cmath.polar(complex(x, y)),
            })
            
            self.last_ans = result
            self.add_to_history(expression, result)
            return result
            
        except Exception as e:
            raise ValueError(f"Erreur d'évaluation: {str(e)}")
    
    def memory_add(self, value):
        """Ajoute une valeur à la mémoire"""
        self.memory += value
        return self.memory
    
    def memory_subtract(self, value):
        """Soustrait une valeur de la mémoire"""
        self.memory -= value
        return self.memory
    
    def memory_clear(self):
        """Réinitialise la mémoire"""
        self.memory = 0
        return self.memory
    
    def memory_recall(self):
        """Récupère la valeur en mémoire"""
        return self.memory
    
    def format_number(self, number):
        """Formate un nombre selon les paramètres actuels"""
        if not isinstance(number, (int, float)):
            return str(number)
            
        if self.settings['number_format'] == 'sci':
            return f"{number:.{self.settings['precision']}e}"
        elif self.settings['number_format'] == 'eng':
            # Format d'ingénierie (exposants multiples de 3)
            if number == 0:
                return "0"
                
            exp = math.floor(math.log10(abs(number)))
            exp = exp - (exp % 3)
            mantissa = number / (10 ** exp)
            
            return f"{mantissa:.{self.settings['precision']}f}e{exp}"
        else:
            # Format normal
            if number == int(number):
                return str(int(number))
            return f"{number:.{self.settings['precision']}f}".rstrip('0').rstrip('.')
    
    def set_precision(self, precision):
        """Définit la précision d'affichage"""
        if 0 <= precision <= 15:
            self.settings['precision'] = precision
            return True
        return False
    
    def set_number_format(self, fmt):
        """Définit le format des nombres (normal, sci, eng)"""
        if fmt in ['normal', 'sci', 'eng']:
            self.settings['number_format'] = fmt
            return True
        return False
    
    # Méthodes pour gérer l'historique
    def add_to_history(self, expression, result):
        """
        Ajoute une entrée à l'historique des calculs
        
        Args:
            expression: L'expression calculée
            result: Le résultat du calcul
        """
        self.history.append({
            'timestamp': datetime.now(),
            'expression': expression,
            'result': result
        })
        
        # Limiter la taille de l'historique
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
    
    def get_history(self, limit=None):
        """
        Récupère l'historique des calculs
        
        Args:
            limit: Nombre maximum d'entrées à retourner (None pour tout l'historique)
            
        Returns:
            Liste des entrées d'historique
        """
        if limit is not None and limit > 0:
            return self.history[-limit:]
        return self.history.copy()
    
    def clear_history(self):
        """Efface tout l'historique des calculs"""
        self.history.clear()
    
    def save_history_to_file(self, filename):
        """
        Sauvegarde l'historique dans un fichier
        
        Args:
            filename: Chemin du fichier de sauvegarde
            
        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        try:
            with open(filename, 'w') as f:
                import json
                # Convertir les objets datetime en chaînes pour la sérialisation JSON
                serializable_history = []
                for entry in self.history:
                    serializable_entry = entry.copy()
                    serializable_entry['timestamp'] = entry['timestamp'].isoformat()
                    serializable_history.append(serializable_entry)
                json.dump(serializable_history, f, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
            return False
    
    def load_history_from_file(self, filename):
        """
        Charge l'historique depuis un fichier
        
        Args:
            filename: Chemin du fichier à charger
            
        Returns:
            True si le chargement a réussi, False sinon
        """
        try:
            with open(filename, 'r') as f:
                import json
                serializable_history = json.load(f)
                self.history = []
                for entry in serializable_history:
                    from datetime import datetime
                    self.history.append({
                        'timestamp': datetime.fromisoformat(entry['timestamp']),
                        'expression': entry['expression'],
                        'result': entry['result']
                    })
            return True
        except Exception as e:
            print(f"Erreur lors du chargement de l'historique: {e}")
            return False
    
    # Méthodes statistiques
    def calculate_mean(self, numbers):
        """Calcule la moyenne d'une liste de nombres"""
        if not numbers:
            raise ValueError("La liste des nombres ne peut pas être vide")
        return sum(numbers) / len(numbers)
    
    def calculate_median(self, numbers):
        """Calcule la médiane d'une liste de nombres"""
        if not numbers:
            raise ValueError("La liste des nombres ne peut pas être vide")
            
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        mid = n // 2
        
        if n % 2 == 1:
            return sorted_numbers[mid]
        else:
            return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    
    def calculate_mode(self, numbers):
        """Calcule le(s) mode(s) d'une liste de nombres"""
        if not numbers:
            raise ValueError("La liste des nombres ne peut pas être vide")
            
        frequency = {}
        for num in numbers:
            frequency[num] = frequency.get(num, 0) + 1
        
        max_freq = max(frequency.values())
        modes = [num for num, freq in frequency.items() if freq == max_freq]
        
        return modes[0] if len(modes) == 1 else modes
    
    def calculate_std_dev(self, numbers, sample=False):
        """
        Calcule l'écart-type d'une liste de nombres
        
        Args:
            numbers: Liste de nombres
            sample: Si True, calcule l'écart-type d'échantillon (n-1)
        """
        if not numbers:
            raise ValueError("La liste des nombres ne peut pas être vide")
            
        n = len(numbers)
        if n == 1 and sample:
            return 0.0
            
        mean = self.calculate_mean(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / (n - 1 if sample else n)
        return math.sqrt(variance)
    
    def calculate_variance(self, numbers, sample=False):
        """
        Calcule la variance d'une liste de nombres
        
        Args:
            numbers: Liste de nombres
            sample: Si True, calcule la variance d'échantillon (n-1)
        """
        if not numbers:
            raise ValueError("La liste des nombres ne peut pas être vide")
            
        n = len(numbers)
        if n == 1 and sample:
            return 0.0
            
        mean = self.calculate_mean(numbers)
        return sum((x - mean) ** 2 for x in numbers) / (n - 1 if sample else n)
    
    def calculate_regression(self, x_data, y_data):
        """
        Calcule la régression linéaire (pente et ordonnée à l'origine)
        
        Returns:
            Tuple (slope, intercept, r_squared)
        """
        if len(x_data) != len(y_data):
            raise ValueError("Les listes x et y doivent avoir la même longueur")
        if len(x_data) < 2:
            raise ValueError("Au moins deux points sont nécessaires pour la régression")
            
        n = len(x_data)
        sum_x = sum(x_data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_data, y_data))
        sum_x2 = sum(x ** 2 for x in x_data)
        
        # Calcul de la pente (slope) et de l'ordonnée à l'origine (intercept)
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            raise ValueError("Les points sont alignés verticalement")
            
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n
        
        # Calcul du coefficient de détermination (R²)
        y_mean = sum_y / n
        ss_total = sum((y - y_mean) ** 2 for y in y_data)
        ss_residual = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_data, y_data))
        r_squared = 1 - (ss_residual / ss_total) if ss_total != 0 else 1.0
        
        return slope, intercept, r_squared
