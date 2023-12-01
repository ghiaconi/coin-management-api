import requests
from datetime import datetime, timedelta
from ..models.token import db, Token
from ..utils.exceptions import *


class TokenService:
    coingecko_base_url = 'https://api.coingecko.com/api/v3'
    coin_endpoint = f'{coingecko_base_url}/coins/'

    def get_or_create_token(self, token_key):
        existing_token = Token.query.filter_by(key=token_key).first()
        try:
            if not existing_token:
                data = self.create_token(token_key)
                if data:
                    existing_token = data
                else:
                    raise TokenServiceError(f'Error creating token: {data}')
            else:
                return existing_token

        except TokenServiceError as e:
            raise TokenNotFoundError(f'Token not found: {e}')

        return existing_token

    def create_token(self, token_key):
        try:
            token_info = self.fetch_token_data(token_key)

            new_token = Token(
                key=token_info.get('id', token_key),
                attributes=token_info
            )

            db.session.add(new_token)
            db.session.commit()

            return new_token

        except TokenNotFoundError as e:
            raise e

    def fetch_token_data(self, token_key):
        params = {
            'localization': 'false',
            'community_data': 'false',
            'developer_data': 'false',
            'sparkline': 'true',
        }

        try:
            response = requests.get(self.coin_endpoint + token_key, params=params)
            response.raise_for_status()

            token_info = response.json()

            if token_info:
                return token_info
            else:
                raise TokenNotFoundError(f'Token not found: {token_key}')
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise TokenNotFoundError(f'Token not found: {token_key}')
            else:
                raise TokenServiceError(f'Request error occurred: {str(e)}')
        except requests.Timeout:
            raise TokenServiceError('Timeout error occurred.')
        except requests.RequestException as e:
            raise TokenServiceError(f'Request error occurred: {str(e)}')

    # def populate_table_with_popular_tokens(self):
    #     popular_tokens = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano']
    #     results = []
    #
    #     for token_key in popular_tokens:
    #         res, data = self.create_token(token_key)
    #         results.append((res, data))
    #
    #     return results

    # def update_existing_tokens(self):  # TODO: add to a cron job
    #     try:
    #         existing_tokens = Token.query.all()
    #
    #         for token in existing_tokens:
    #             last_update_time = token.last_update_time or datetime(1970, 1, 1)
    #             time_since_last_update = datetime.utcnow() - last_update_time
    #
    #             if time_since_last_update > timedelta(hours=24):
    #                 token_info = self.get_token_data(token.key)
    #
    #                 if token_info:
    #                     token.attributes = token_info['attributes']
    #                     token.last_update_time = datetime.utcnow()
    #
    #         db.session.commit()
    #     except Exception as e:
    #         print(f"Error updating tokens: {str(e)}")

