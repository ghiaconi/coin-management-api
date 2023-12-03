from flask_restx import Namespace, Resource, reqparse, fields
from app.models.token import Token as TokenModel
from app.services.token_service import TokenService
from app.utils.exceptions import *

ns = Namespace('tokens', description='Token related operations')
token_service = TokenService()

token_parser = reqparse.RequestParser()
token_parser.add_argument('data', type=str, help='Token data')

query_parser = reqparse.RequestParser()
query_parser.add_argument('key', type=str, help='Filter tokens by name')

# Swagger documentation for the Token model
token_model = ns.model('Token', {
    'id': fields.String(description='Token ID'),
    'name': fields.String(description='Token name'),
    'symbol': fields.String(description='Token symbol'),
    'market_cap_rank': fields.Integer(description='Token market cap rank'),
    'current_price': fields.Float(description='Token current price'),
    'market_cap': fields.Integer(description='Token market cap'),
    'total_volume': fields.Integer(description='Token total volume'),
    'high_24h': fields.Float(description='Token high 24h'),
    'low_24h': fields.Float(description='Token low 24h'),
    'price_change_24h': fields.Float(description='Token price change 24h'),
    'price_change_percentage_24h': fields.Float(description='Token price change percentage 24h'),
    'market_cap_change_24h': fields.Float(description='Token market cap change 24h'),
    'market_cap_change_percentage_24h': fields.Float(description='Token market cap change percentage 24h'),
    'circulating_supply': fields.Integer(description='Token circulating supply'),
    'total_supply': fields.Integer(description='Token total supply'),
    'ath': fields.Float(description='Token all time high'),
    'ath_change_percentage': fields.Float(description='Token all time high change percentage'),
    'ath_date': fields.DateTime(description='Token all time high date'),
    'atl': fields.Float(description='Token all time low'),
    'atl_change_percentage': fields.Float(description='Token all time low change percentage'),
    'atl_date': fields.DateTime(description='Token all time low date'),
    'roi': fields.Nested({
        'times': fields.Float(description='Token ROI times'),
        'currency': fields.String(description='Token ROI currency'),
        'percentage': fields.Float(description='Token ROI percentage'),
    }, description='Token ROI'),
    'last_updated': fields.DateTime(description='Token last updated'),
})


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
