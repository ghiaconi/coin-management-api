from flask_restx import Namespace, Resource, reqparse

ns = Namespace('tokens', description='Token related operations')

token_parser = reqparse.RequestParser()
token_parser.add_argument('id', type=int, help='User id')
token_parser.add_argument('data', type=str, help='User username')


@ns.route('/')
class TokensResource(Resource):
    def get(self):
        return {'message': 'Hello, Tokens endpoint!'}
