from flask_restx import Namespace, Resource, reqparse, fields, inputs
from app.models.user import db, User as UserModel
from sqlalchemy.exc import IntegrityError
from app.services.user_service import (UserService, TokenNotFoundError, UserNotFoundError, TokenAlreadyAssignedError,
                                       TokenNotAssignedError)

ns = Namespace('users', description='User related operations')
user_service = UserService()

# User validation parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='User username')
user_parser.add_argument('email', type=str, help='User email')
user_parser.add_argument('password', type=str, help='User password')

token_id_parser = reqparse.RequestParser()
token_id_parser.add_argument('token_id', type=str, required=True, help='The username of the user')

# Swagger documentation for the User model
user_model = ns.model('User', {
    'username': fields.String(description='username'),
    'email': fields.String(description='User email'),
    'password': fields.String(description='User password'),
})


@ns.route('/')
class Users(Resource):
    @ns.doc(description='Retrieve all registered users')
    def get(self):
        try:
            users = UserModel.query.all()
            serialized_users = [user.serialize() for user in users]
            return {'users': serialized_users}, 200
        except Exception as e:
            return {'message': 'Error getting users', 'error': str(e)}, 500

    @ns.doc(description='Register a new user')
    @ns.expect(user_model, validate=True, validate_payload=True)
    def post(self):
        user_data = user_parser.parse_args()
        try:
            # Create a new user and add it to the database
            new_user = UserModel(**user_data)
            db.session.add(new_user)
            db.session.commit()

            return {'message': f'User {new_user.username} registered successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'Error registering user', 'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error registering user', 'error': str(e)}, 500


@ns.route('/<username>')
class User(Resource):
    @ns.doc(description='Update user details')
    @ns.expect(user_model, validate=True, validate_payload=True)
    def put(self, username):
        args = user_parser.parse_args()

        try:
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                return {'message': f'User {username} not found'}, 404

            if 'username' in args and args['username'] is not None:
                user.username = args['username']
            if 'email' in args and args['email'] is not None:
                user.email = args['email']
            if 'password' in args and args['password'] is not None:
                user.password = args['password']

            db.session.commit()
            return {'message': f'User details updated for user {username}'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating user details for user {username}', 'error': str(e)}, 500

    @ns.doc(description='Delete user by username')
    def delete(self, username):
        try:
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                return {'message': f'User with username {username} not found'}, 404

            db.session.delete(user)
            db.session.commit()

            return {'message': f'User {username} deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting user {username}', 'error': str(e)}, 500

    @ns.doc(description='Get user details by username',
            params={'include_tokens': {'description': 'Include monitored tokens', 'type': 'boolean', 'default': False}})
    def get(self, username):
        ns_parser = reqparse.RequestParser()
        ns_parser.add_argument('include_tokens', type=inputs.boolean, required=True, help='The token id')

        args = ns_parser.parse_args()
        include_tokens = args.get('include_tokens', False)
        try:
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                return {'message': f'User with username {args} not found'}, 404

            user_data = user.serialize(include_tokens=include_tokens)
            return {'message': f'User details for {username}', 'data': user_data}, 200
        except Exception as e:
            return {'message': f'Error retrieving user details for {username}', 'error': str(e)}, 500


@ns.route('/<username>/tokens/add')
class AssignToken(Resource):
    @ns.doc(description='Add token to the monitored tokens list for user',
            params={'token_id': {'description': 'Id of the token to add to the monitored list', 'type': 'string',
                                 'required': True}})
    def post(self, username):
        args = token_id_parser.parse_args()
        token_id = args['token_id']

        try:
            if user_service.is_token_assigned_to_user(username, token_id):
                return {'message': f'Token {token_id} is already monitored by user {username}'}, 409

            user_service.assign_token_to_user(username, token_id)
            return {'message': f'Token {token_id} successfully added to users {username}\'s list'}, 200

        except (TokenNotFoundError, UserNotFoundError, TokenAlreadyAssignedError) as e:
            return {'message': str(e)}, 404
        except TokenAlreadyAssignedError as e:
            return {'message': str(e)}, 409


@ns.route('/<username>/tokens/remove')
class AssignToken(Resource):
    @ns.doc(description='Remove token from the monitored tokens list for user',
            params={'token_id': {'description': 'Monitored token id to remove', 'type': 'string', 'required': True}})
    def delete(self, username):
        args = token_id_parser.parse_args()
        token_id = args['token_id']

        try:
            user_service.remove_token_from_user(username, token_id)
            return {'message': f'Token {token_id} successfully removed from {username}\'s monitor list'}, 200

        except (TokenNotFoundError, UserNotFoundError, TokenNotAssignedError) as e:
            return {'message': str(e)}, 404
