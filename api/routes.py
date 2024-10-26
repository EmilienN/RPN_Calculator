import logging
from flask_restx import Namespace, Resource
from core.calculator_operations import CalculatorWorkflow
from .models import ApiModels
import uuid
from typing import Dict

logger = logging.getLogger(__name__)

class RPNController:
    def __init__(self):
        self._calculators: Dict[str, CalculatorWorkflow] = {}
        logger.info("RPNController initialisé")

    def get_calculator(self, stack_id: str) -> CalculatorWorkflow:
        calculator = self._calculators.get(stack_id)
        if not calculator:
            logger.warning(f"Tentative d'accès à une pile inexistante: {stack_id}")
            raise ValueError(f"Stack {stack_id} not found")
        return calculator

    def create_calculator(self) -> tuple[str, CalculatorWorkflow]:
        stack_id = str(uuid.uuid4())
        calculator = CalculatorWorkflow()
        self._calculators[stack_id] = calculator
        logger.info(f"Nouvelle pile créée avec l'ID: {stack_id}")
        return stack_id, calculator

    def delete_calculator(self, stack_id: str) -> None:
        if stack_id in self._calculators:
            del self._calculators[stack_id]
            logger.info(f"Pile supprimée: {stack_id}")
        else:
            logger.warning(f"Tentative de suppression d'une pile inexistante: {stack_id}")

    def get_all_calculators(self) -> Dict[str, CalculatorWorkflow]:
        logger.info(f"Récupération de toutes les piles. Nombre de piles: {len(self._calculators)}")
        return self._calculators

def create_routes(api):
    rpn = Namespace('rpn', description='Opérations RPN')
    models = ApiModels(rpn)
    controller = RPNController()
    logger.info("Routes RPN créées")

    @rpn.route('/op')
    class OperandList(Resource):
        def get(self):
            logger.info("Liste des opérateurs demandée")
            return {'operators': ['+', '-', '*', '/']}

    @rpn.route('/op/<string:operator>/stack/<string:stack_id>')
    @rpn.param('operator', 'Opérateur à appliquer (+, -, *, /)')
    @rpn.param('stack_id', 'Identifiant de la pile')
    class OperandExecution(Resource):
        @rpn.marshal_with(models.calculator_response)
        def post(self, operator, stack_id):
            logger.info(f"Exécution de l'opérateur '{operator}' sur la pile {stack_id}")
            try:
                calculator = controller.get_calculator(stack_id)
                stack = calculator.run_operation(operator)
                return {'stack_id': stack_id, 'stack': stack}
            except ValueError as e:
                logger.error(f"Erreur lors de l'exécution de l'opérateur: {str(e)}")
                rpn.abort(400, str(e))

    @rpn.route('/stack')
    class Stacks(Resource):
        @rpn.marshal_with(models.calculator_response)
        def post(self):
            """Crée une nouvelle pile"""
            stack_id, calculator = controller.create_calculator()
            return {
                'stack_id': stack_id,
                'stack': calculator.calculator.get_stack()
            }

        @rpn.marshal_list_with(models.calculator_response)
        def get(self):
            """Liste toutes les piles disponibles"""
            calculators = controller.get_all_calculators()
            return [
                {'stack_id': calc_id, 'stack': calc.calculator.get_stack()}
                for calc_id, calc in calculators.items()
            ]

    @rpn.route('/stack/<string:stack_id>')
    @rpn.param('stack_id', 'Identifiant de la pile')
    class Stack(Resource):
        @rpn.marshal_with(models.calculator_response)
        def get(self, stack_id):
            """Récupère une pile spécifique"""
            try:
                calculator = controller.get_calculator(stack_id)
                return {
                    'stack_id': stack_id,
                    'stack': calculator.calculator.get_stack()
                }
            except ValueError as e:
                rpn.abort(404, str(e))

        @rpn.expect(models.push_request, validate=True)
        @rpn.marshal_with(models.calculator_response)
        def post(self, stack_id):
            """Ajoute une valeur à la pile"""
            try:
                calculator = controller.get_calculator(stack_id)
                value = rpn.payload['value']
                stack = calculator.run_operation(operation=None, value=value)
                return {
                    'stack_id': stack_id,
                    'stack': stack
                }
            except ValueError as e:
                rpn.abort(400, str(e))

        def delete(self, stack_id):
            """Supprime une pile"""
            try:
                controller.get_calculator(stack_id)
                controller.delete_calculator(stack_id)
                return '', 204
            except ValueError as e:
                rpn.abort(404, str(e))

    @rpn.route('/stack/<string:stack_id>/pop')
    @rpn.param('stack_id', 'Identifiant de la pile')
    class StackPop(Resource):
        @rpn.marshal_with(models.calculator_response)
        def delete(self, stack_id):
            """Supprime la dernière valeur de la pile"""
            try:
                calculator = controller.get_calculator(stack_id)
                stack = calculator.delete_last_value()
                return {
                    'stack_id': stack_id,
                    'stack': stack
                }
            except ValueError as e:
                rpn.abort(404, str(e))
            except IndexError:
                rpn.abort(400, "Stack is empty")

    return rpn
