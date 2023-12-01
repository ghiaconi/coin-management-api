import requests
from ..models.user import db, User
from ..models.token import Token
from app.services.token_service import TokenService
from ..utils.exceptions import *

token_service = TokenService()


class UserService:
    def assign_token_to_user(self, username, token_id):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UserNotFoundError(f'User {username} not found')

        token = token_service.get_or_create_token(token_id)
        if not token:
            raise TokenNotFoundError(f'Token {token_id} not found')

        if token in user.tokens:
            raise TokenAlreadyAssignedError(f'Token {token_id} is already assigned to user {username}')

        user.assign_token(token)

    def is_token_assigned_to_user(self, username, token_id):
        user = User.query.filter_by(username=username).first()
        token = Token.query.filter_by(key=token_id).first()

        if not user or not token:
            return False

        return token in user.tokens

    def remove_token_from_user(self, username, token_id):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UserNotFoundError(f'User {username} not found')

        token = Token.query.filter_by(key=token_id).first()
        if not token:
            raise TokenNotFoundError(f'Token {token_id} not found')

        if token not in user.tokens:
            raise TokenNotAssignedError(f'Token {token_id} is not assigned to user {username}')

        user.unlink_token(token)

    def get_monitored_tokens(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UserNotFoundError(f'User {username} not found')

        tokens = user.tokens
        return [token.serialize() for token in tokens]


    def get_archived_tokens(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UserNotFoundError(f'User {username} not found')
        token_ids = user.archived_tokens_refs.keys()
        tokens = Token.query.filter(Token.key.in_(token_ids)).all()

        return [token.serialize() for token in tokens]

