from core.rpn_calculator_core import RPNCalculator  

class CalculatorWorkflow:
    def __init__(self):
        self.calculator = RPNCalculator()
    
    def run_operation(self, operation: str, value: float = None):
        if value is not None:
            self.calculator.push(value)
        else:
            self.calculator.operate(operation)
        return self.calculator.get_stack()
    
    def delete_last_value(self):
        self.calculator.delete_last_value()
        return self.calculator.get_stack()
    
    def clear_stack(self):
        self.calculator.clear()
        return self.calculator.get_stack()