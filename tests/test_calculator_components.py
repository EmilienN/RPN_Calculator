# test_calculator.py
import pytest
from core.rpn_calculator_core import RPNCalculator
from core.calculator_operations import CalculatorWorkflow

# Tests for RPNCalculator class
class TestRPNCalculator:
    @pytest.fixture
    def calculator(self):
        return RPNCalculator()

    def test_push_single_value(self, calculator):
        calculator.push(5.0)
        assert calculator.get_stack() == [5.0]

    def test_push_multiple_values(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        assert calculator.get_stack() == [5.0, 3.0]

    def test_clear_stack(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        calculator.clear()
        assert calculator.get_stack() == []

    def test_addition(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        calculator.operate('+')
        assert calculator.get_stack() == [8.0]

    def test_subtraction(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        calculator.operate('-')
        assert calculator.get_stack() == [2.0]

    def test_multiplication(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        calculator.operate('*')
        assert calculator.get_stack() == [15.0]

    def test_division(self, calculator):
        calculator.push(6.0)
        calculator.push(2.0)
        calculator.operate('/')
        assert calculator.get_stack() == [3.0]

    def test_division_by_zero(self, calculator):
        calculator.push(6.0)
        calculator.push(0.0)
        with pytest.raises(ValueError):
            calculator.operate('/')

    def test_insufficient_operands(self, calculator):
        calculator.push(5.0)
        with pytest.raises(ValueError, match="Insufficient operands"):
            calculator.operate('+')

    def test_unknown_operator(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        with pytest.raises(ValueError, match="Unknown operator"):
            calculator.operate('%')

    def test_stack_independence(self, calculator):
        original_stack = calculator.get_stack()
        original_stack.append(42.0)
        assert calculator.get_stack() != original_stack

    def test_delete_last_value(self, calculator):
        calculator.push(5.0)
        calculator.push(3.0)
        calculator.delete_last_value()
        assert calculator.get_stack() == [5.0]

# CalculatorWorkflow tests
class TestCalculatorWorkflow:
    @pytest.fixture
    def workflow(self):
        return CalculatorWorkflow()

    def test_push_operation(self, workflow):
        result = workflow.run_operation(operation='+', value=5.0)
        assert result == [5.0]

    def test_clear_stack(self, workflow):
        workflow.run_operation(operation='+', value=5.0)
        result = workflow.clear_stack()
        assert result == []
    
    def test_delete_last_value(self, workflow):
        workflow.run_operation(operation='+', value=5.0)
        workflow.run_operation(operation='+', value=3.0)
        result = workflow.delete_last_value()
        assert result == [5.0]

    def test_complex_calculation(self, workflow):
        # Test a more complex calculation: (5 + 3) * 2
        workflow.run_operation(operation='+', value=5.0)
        workflow.run_operation(operation='+', value=3.0)
        workflow.run_operation(operation='+')  # 5 + 3 = 8
        workflow.run_operation(operation='+', value=2.0)
        result = workflow.run_operation(operation='*')  # 8 * 2 = 16
        assert result == [16.0]

    def test_multiple_operations(self, workflow):
        # Push some numbers and perform multiple operations
        workflow.run_operation(operation='+', value=10.0)
        workflow.run_operation(operation='+', value=5.0)
        workflow.run_operation(operation='-')  # 10 - 5 = 5
        workflow.run_operation(operation='+', value=3.0)
        result = workflow.run_operation(operation='*')  # 5 * 3 = 15
        assert result == [15.0]

    def test_workflow_error_handling(self, workflow):
        workflow.run_operation(operation='+', value=5.0)
        with pytest.raises(ValueError, match="Insufficient operands"):
            workflow.run_operation(operation='+')

# Test integration between calculator components
class TestCalculatorIntegration:
    def test_full_calculation_workflow(self):
        workflow = CalculatorWorkflow()
        
        # Test a complex calculation: ((15 + 5) * 2) / 10
        steps = [
            ('+', 15.0),  # Push 15
            ('+', 5.0),   # Push 5
            ('+', None),  # Add: 15 + 5 = 20
            ('+', 2.0),   # Push 2
            ('*', None),  # Multiply: 20 * 2 = 40
            ('+', 10.0),  # Push 10
            ('/', None),  # Divide: 40 / 10 = 4
        ]
        
        for operation, value in steps:
            result = workflow.run_operation(operation=operation, value=value)
        
        assert result == [4.0]

    def test_state_persistence(self):
        workflow = CalculatorWorkflow()
        
        # Perform operations and verify state is maintained
        workflow.run_operation(operation='+', value=10.0)
        workflow.run_operation(operation='+', value=20.0)
        intermediate_result = workflow.run_operation(operation='+')  # 10 + 20 = 30
        assert intermediate_result == [30.0]
        
        # Continue with more operations
        workflow.run_operation(operation='+', value=5.0)
        final_result = workflow.run_operation(operation='*')  # 30 * 5 = 150
        assert final_result == [150.0]

