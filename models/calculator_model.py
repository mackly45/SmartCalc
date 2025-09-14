class CalculatorModel:
    def __init__(self):
        self.current_value = '0'
        self.expression = ''
        self.memory = 0

    def clear(self):
        self.current_value = '0'
        self.expression = ''

    def append_number(self, number):
        if self.current_value == '0' and number != '.':
            self.current_value = str(number)
        else:
            self.current_value += str(number)
        
        if self.expression == '0' or self.expression.endswith('='):
            self.expression = self.current_value
        else:
            self.expression += str(number)

    def add_operator(self, operator):
        if self.expression.endswith(('+', '-', '*', '/', '=')):
            self.expression = self.expression[:-1] + operator
        else:
            self.expression += operator
        self.current_value = '0'

    def calculate(self):
        try:
            # If we have a current value but no expression, use it as the first operand
            if not self.expression and self.current_value:
                self.expression = self.current_value
            
            # If expression ends with an operator, remove it before evaluating
            if self.expression and self.expression[-1] in '+-×÷':
                self.expression = self.expression[:-1]
            
            if self.expression:
                # Replace display operators with Python operators
                eval_expr = self.expression.replace('×', '*').replace('÷', '/')
                result = str(eval(eval_expr))
                self.expression = self.expression + '=' + result
                self.current_value = result
        except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
            print(f"Error in calculation: {e}")
            self.current_value = 'Error'
            self.expression = ''

    def add_decimal(self):
        if '.' not in self.current_value:
            self.current_value += '.'
            self.expression = self.current_value if self.expression == '0' else self.expression + '.'

    def percentage(self):
        try:
            value = float(self.current_value) / 100
            self.current_value = str(value)
            self.expression = self.current_value
        except:
            self.current_value = 'Error'
            self.expression = ''

    def toggle_sign(self):
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = '-' + self.current_value
        
        if '=' in self.expression:
            self.expression = self.current_value
        else:
            # Update the last number in the expression
            parts = []
            temp = ''
            for char in self.expression:
                if char in '+-*/':
                    if temp:
                        parts.append(temp)
                        temp = ''
                    parts.append(char)
                else:
                    temp += char
            if temp:
                parts.append(temp)
            
            if parts and parts[-1].lstrip('-').replace('.', '').isdigit():
                parts[-1] = self.current_value
                self.expression = ''.join(parts)
            else:
                self.expression = self.current_value
