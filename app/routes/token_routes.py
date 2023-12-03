from flask_restx import Namespace, Resource, reqparse, fields, inputs
from app.models.token import Token as TokenModel
from app.services.token_service import TokenService
from app.utils.exceptions import *

ns = Namespace('tokens', description='Token related operations')
token_service = TokenService()

token_parser = reqparse.RequestParser()
token_parser.add_argument('data', type=str, help='Token data')

query_parser = reqparse.RequestParser()
query_parser.add_argument('key', type=str, help='Filter tokens by name')


@ns.route('/')
class Tokens(Resource):
    @ns.doc(description='Retrieve all tokens')
    def get(self):
        try:
            tokens = TokenModel.query.order_by(TokenModel.market_cap_rank.asc()).all()

            response_data = [token.serialize() for token in tokens]
            return {'total_records': len(response_data), 'data': response_data}
        except Exception as e:
            return {'message': f'Error: {str(e)}'}, 500


@ns.route('/<token_key>')
class Token(Resource):
    @ns.doc(description='Retrieve a specific token by its ID')
    def get(self, token_key):
        try:
            token = token_service.get_or_create_token(token_key)

            if token:
                token_data = token.serialize()
                return {'data': token_data}
            else:
                return {'message': f'Token not found: {token_key}'}, 404

        except TokenNotFoundError as e:
            return {'message': f'Token not found: {str(e)}'}, 404

        except TokenServiceError as e:
            return {'message': f'Token service error: {str(e)}'}, 500


@ns.route('/update_tokens')
class RefreshTokens(Resource):
    @ns.doc(description='Update stored tokens with fresh data from the API')
    def get(self):
        try:
            res, time = token_service.refresh_tokens()
            return {'message': time}, 200

        except TokenServiceError as e:
            return {'message': f'Token service error: {str(e)}'}, 500
