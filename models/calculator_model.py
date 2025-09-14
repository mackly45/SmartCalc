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
            # Replace × with * and ÷ with / for evaluation
            eval_expr = self.expression.replace('×', '*').replace('÷', '/')
            # If expression ends with an operator, remove it before evaluating
            if eval_expr and eval_expr[-1] in '+-*/':
                eval_expr = eval_expr[:-1]
            if eval_expr:  # Only evaluate if there's something to evaluate
                result = str(eval(eval_expr))
                self.expression = eval_expr + '=' + result
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
