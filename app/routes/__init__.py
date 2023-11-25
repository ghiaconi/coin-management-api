from flask import Blueprint
from flask_restx import Api

# Load namespaces
from .user_routes import ns as users_api
from .token_routes import ns as tokens_api

blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    version='1.0',
    title='Coin Management API',
    description='A simple Coin Management API, used to manage users and their coin configurations. Makes use of '
                'Coingecko\'s API to fetch coin data.',
    doc='/',  # Set the Swagger UI endpoint to root
    prefix='/api/v1'  # Set the API prefix to /api/v1
)

# Initialize namespaces
api.add_namespace(users_api, path='/users')
api.add_namespace(tokens_api, path='/tokens')
