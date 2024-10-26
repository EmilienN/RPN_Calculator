"""Module principal pour l'application de calculatrice RPN."""

import logging
from flask import Flask, redirect
from flask_restx import Api

from api.routes import create_routes


def configure_logging():
    """Configure le logging pour l'application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='rpn_calculator.log'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)


def create_app():
    """Crée et configure l'application Flask."""
    configure_logging()
    app = Flask(__name__)
    logging.info("Application Flask créée")
    
    api = Api(
        app,
        version='1.0',
        title='RPN Calculator API',
        description='API pour calculatrice RPN',
        doc='/'
    )
    logging.info("API Flask-RESTX configurée")

    rpn = create_routes(api)
    api.add_namespace(rpn, path='/rpn')
    logging.info("Routes RPN ajoutées à l'API")

    @app.route('/')
    def index():
        """Route racine redirigeant vers Swagger UI."""
        logging.info("Redirection vers Swagger UI")
        return redirect('/swagger')

    return app


app = create_app()

if __name__ == '__main__':
    logging.info("Démarrage de l'application")
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False
    )