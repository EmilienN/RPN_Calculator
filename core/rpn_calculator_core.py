from typing import List
from core.calculator_state import CalculatorState

class RPNCalculator:
    def __init__(self):
        self.state = CalculatorState()
    
    def push(self, value: float) -> None:
        """Push a number onto the stack"""
        self.state.stack.append(value)
    
    def operate(self, operator: str) -> None:
        """Perform operation on the last two numbers in the stack"""
        if len(self.state.stack) < 2:
            raise ValueError("Insufficient operands")
        
        b = self.state.stack.pop()
        a = self.state.stack.pop()
        
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y
        }
        
        if operator not in operations:
            raise ValueError(f"Unknown operator: {operator}")
        
        if operator == '/' and b == 0:
            raise ValueError("Division by zero")
        
        result = operations[operator](a, b)
        self.state.stack.append(result)
    
    def get_stack(self) -> List[float]:
        """Return current stack"""
        return self.state.stack.copy()
    
    def delete_last_value(self) -> None:
        """Delete the last value in the stack"""
        self.state.stack.pop()
    
    def clear(self) -> None:
        """Clear the stack"""
        self.state.stack.clear()
