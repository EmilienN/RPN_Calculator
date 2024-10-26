"""Main module for the RPN calculator application."""

import logging
from flask import Flask, redirect
from flask_restx import Api

from api.routes import create_routes


def configure_logging():
    """Configure logging for the application."""
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
    """Create and configure the Flask application."""
    configure_logging()
    app = Flask(__name__)
    logging.info("Flask application created")
    
    api = Api(
        app,
        version='1.0',
        title='RPN Calculator API',
        description='API for RPN calculator',
        doc='/'
    )
    logging.info("Flask-RESTX API configured")

    rpn = create_routes(api)
    api.add_namespace(rpn, path='/rpn')
    logging.info("RPN routes added to API")

    @app.route('/')
    def index():
        """Root route redirecting to Swagger UI."""
        logging.info("Redirecting to Swagger UI")
        return redirect('/swagger')

    return app


app = create_app()

if __name__ == '__main__':
    logging.info("Starting the application")
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False
    )