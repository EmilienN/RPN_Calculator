from flask_restx import fields, Model

class ApiModels:
    def __init__(self, api):
        self.calculator_response = api.model('CalculatorResponse', {
            'stack_id': fields.String(description='Identifiant unique de la pile'),
            'stack': fields.List(fields.Float, description='Valeurs dans la pile')
        })

        self.push_request = api.model('PushRequest', {
            'value': fields.Float(required=True, description='Valeur à ajouter à la pile')
        })