import requests
from datetime import datetime, timedelta, timezone
from ..models.token import db, Token
from ..utils.exceptions import *


class TokenService:
    coingecko_base_url = 'https://api.coingecko.com/api/v3'
    coin_endpoint = f'{coingecko_base_url}/coins/'
    markets_endpoint = f'{coingecko_base_url}/coins/markets'
    calls_per_minute_limit = 30
    data_refreshed_every = 60  # seconds
    items_per_page_limit = 250

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
            token_info = self.fetch_tokens_market_data(token_key)[0]

            new_token = Token(
                key=token_info.get('id', token_key),
                attributes=token_info
            )

            db.session.add(new_token)
            db.session.commit()

            return new_token

        except TokenNotFoundError as e:
            raise e

    # TODO split in 2 or use the dedicated /coin endpoint when searching for one token
    def fetch_tokens_market_data(self, ids, page=1):
        ids_to_query = ','.join([ids] if not isinstance(ids, list) else ids)

        params = {
            'ids': ids_to_query,
            'vs_currency': 'eur',
            'order': 'market_cap_desc',
            'per_page': self.items_per_page_limit,
            'page': page,
            'sparkline': 'true',
        }

        try:
            response = requests.get(self.markets_endpoint, params=params)
            response.raise_for_status()
            tokens_data = response.json()

            if len(tokens_data) == 0:
                raise TokenNotFoundError(f'Token not found: {ids}')

            return response.json()

        except requests.HTTPError as e:
            raise TokenServiceError(f'Request error occurred: {str(e)}')

        except requests.Timeout:
            raise TokenServiceError('Timeout error occurred.')

        except requests.RequestException as e:
            raise TokenServiceError(f'Request error occurred: {str(e)}')

    # def refresh_tokens(self):  # TODO: add to a cron job
    #     try:
    #         existing_tokens = Token.query.all()
    #
    #         for token in existing_tokens:
    #             last_update_str = token.attributes['last_updated'] or datetime(1970, 1, 1)
    #             last_update = datetime.strptime(last_update_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    #             current_time = datetime.now(timezone.utc)
    #             time_since_last_update = current_time - last_update
    #
    #             if time_since_last_update > timedelta(hours=24):
    #                 token_info = self.fetch_tokens_market_data(token.key)
    #
    #                 if token_info:
    #                     token.attributes = token_info['attributes']
    #                     token.last_update_time = datetime.utcnow()
    #
    #         db.session.commit()
    #     except Exception as e:
    #         print(f"Error updating tokens: {str(e)}")
    #
    # def update_expired_tokens(self):
    #     # Sort tokens based on the oldest last_update_time
    #     sorted_tokens = sorted(token_data.items(), key=lambda x: x[1]['last_update_time'])
    #
    #     # Batch tokens based on the rate limit (30 calls/minute)
    #     batch_size = items_per_page_limit
    #     for i in range(0, len(sorted_tokens), batch_size):
    #         batch_tokens = dict(sorted_tokens[i:i + batch_size])
    #         for token in batch_tokens:
    #             fetch_data_for_token(token)
