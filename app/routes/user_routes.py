from flask_restx import Namespace, Resource, reqparse, fields, inputs
from app.models.user import db, User as UserModel
from sqlalchemy.exc import IntegrityError

ns = Namespace('users', description='User related operations')

# User validation parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='User username')
user_parser.add_argument('email', type=str, help='User email')
user_parser.add_argument('password', type=str, help='User password')

# Custom fields validation parser
ns_parser = reqparse.RequestParser()
ns_parser.add_argument('include_tokens', type=inputs.boolean, required=True, help='The username of the user')

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
