class CalculatorModel:
    def __init__(self):
        self.current_value = '0'
        self.expression = ''
        self.memory = 0
        self.waiting_for_operand = True

    def clear(self):
        self.current_value = '0'
        self.expression = ''
        self.waiting_for_operand = True

    def append_number(self, number):
        if self.waiting_for_operand:
            self.current_value = str(number)
            self.waiting_for_operand = False
        else:
            self.current_value += str(number)

    def add_operator(self, operator):
        if not self.expression and not self.current_value:
            return
            
        # If we're starting a new expression, use the current value
        if not self.expression and self.current_value:
            self.expression = self.current_value
        # If we already have an expression and a current value, append it
        elif not self.waiting_for_operand and self.current_value:
            self.expression += self.current_value
        # If we're replacing an operator, remove the last one
        elif self.waiting_for_operand and self.expression and self.expression[-1] in '+-×÷':
            self.expression = self.expression[:-1]
            
        # Add the new operator
        self.expression += operator
        self.waiting_for_operand = True
        self.current_value = ''

    def calculate(self):
        if not self.expression and not self.current_value:
            return
            
        try:
            # Build the complete expression
            if not self.waiting_for_operand and self.current_value:
                self.expression += self.current_value
            
            # Replace display operators with Python operators
            eval_expr = self.expression.replace('×', '*').replace('÷', '/')
            
            # Remove any trailing operators
            while eval_expr and eval_expr[-1] in '+-*/':
                eval_expr = eval_expr[:-1]
                
            if eval_expr:
                result = str(eval(eval_expr))
                self.expression = ''
                self.current_value = result
                self.waiting_for_operand = True
                
        except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
            print(f"Error in calculation: {e}")
            self.current_value = 'Error'
            self.expression = ''
            self.waiting_for_operand = True

    def add_decimal(self):
        if self.waiting_for_operand:
            self.current_value = '0.'
            self.waiting_for_operand = False
        elif '.' not in self.current_value:
            self.current_value += '.'

    def percentage(self):
        try:
            value = float(self.current_value) / 100
            self.current_value = str(value)
            self.waiting_for_operand = False
        except (ValueError, TypeError):
            self.current_value = 'Error'

    def toggle_sign(self):
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        elif self.current_value != '0':
            self.current_value = '-' + self.current_value
