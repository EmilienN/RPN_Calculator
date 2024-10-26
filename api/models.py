from flask_restx import fields, Model

class ApiModels:
    """API models for calculator operations."""

    def __init__(self, api):
        self.calculator_response = api.model('CalculatorResponse', {
            'stack_id': fields.String(description='Unique stack identifier'),
            'stack': fields.List(fields.Float, description='Values in the stack')
        })

        self.push_request = api.model('PushRequest', {
            'value': fields.Float(required=True, description='Value to add to the stack')
        })