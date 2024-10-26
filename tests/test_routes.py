import pytest
from flask import Flask
from flask_testing import TestCase
from flask_restx import Api
from api.routes import create_routes, RPNController
from core.calculator_operations import CalculatorWorkflow

class TestRPNRoutes(TestCase):
    def create_app(self):
        # Create and configure Flask app for testing
        app = Flask(__name__)
        api = Api(app)
        rpn = create_routes(api)
        api.add_namespace(rpn)
        return app

    def test_list_operators(self):
        # Test listing available operators
        response = self.client.get('/rpn/op')
        self.assert200(response)
        self.assertEqual(response.json, {'operators': ['+', '-', '*', '/']})

    def test_create_stack(self):
        # Test creating a new stack
        response = self.client.post('/rpn/stack')
        self.assert200(response)
        self.assertIn('stack_id', response.json)
        self.assertIn('stack', response.json)
        self.assertEqual(response.json['stack'], [])

    def test_push_value(self):
        # First, create a stack
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']

        # Now push a value
        push_response = self.client.post(f'/rpn/stack/{stack_id}', json={'value': 5})
        self.assert200(push_response)
        self.assertEqual(push_response.json['stack'], [5])

    def test_apply_operator(self):
        # Create a stack and push two values
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']
        self.client.post(f'/rpn/stack/{stack_id}', json={'value': 5})
        self.client.post(f'/rpn/stack/{stack_id}', json={'value': 3})

        # Apply addition operator
        op_response = self.client.post(f'/rpn/op/+/stack/{stack_id}')
        self.assert200(op_response)
        self.assertEqual(op_response.json['stack'], [8])

    def test_delete_stack(self):
        # Create a stack
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']

        # Delete the stack
        delete_response = self.client.delete(f'/rpn/stack/{stack_id}')
        self.assertStatus(delete_response, 204)

        # Try to get the deleted stack
        get_response = self.client.get(f'/rpn/stack/{stack_id}')
        self.assert404(get_response)

    def test_pop_value(self):
        # Create a stack and push a value
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']
        self.client.post(f'/rpn/stack/{stack_id}', json={'value': 5})

        # Pop the value
        pop_response = self.client.delete(f'/rpn/stack/{stack_id}/pop')
        self.assert200(pop_response)
        self.assertEqual(pop_response.json['stack'], [])

    def test_pop_empty_stack(self):
        # Create an empty stack
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']

        # Try to pop from empty stack
        pop_response = self.client.delete(f'/rpn/stack/{stack_id}/pop')
        self.assert400(pop_response)

    def test_get_nonexistent_stack(self):
        response = self.client.get('/rpn/stack/nonexistent-id')
        self.assert404(response)

    def test_apply_operator_to_empty_stack(self):
        # Créer une pile vide
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']

        # Essayer d'appliquer un opérateur
        op_response = self.client.post(f'/rpn/op/+/stack/{stack_id}')
        self.assert400(op_response)

    def test_apply_invalid_operator(self):
        # Créer une pile et ajouter des valeurs
        create_response = self.client.post('/rpn/stack')
        stack_id = create_response.json['stack_id']
        self.client.post(f'/rpn/stack/{stack_id}', json={'value': 5})
        self.client.post(f'/rpn/stack/{stack_id}', json={'value': 3})

        # Essayer d'appliquer un opérateur invalide
        op_response = self.client.post(f'/rpn/op/invalid/stack/{stack_id}')
        self.assert400(op_response)

    def test_get_all_stacks(self):
        # Créer quelques piles
        self.client.post('/rpn/stack')
        self.client.post('/rpn/stack')

        # Récupérer toutes les piles
        response = self.client.get('/rpn/stack')
        self.assert200(response)
        self.assertGreaterEqual(len(response.json), 2)
