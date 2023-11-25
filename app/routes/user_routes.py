from flask_restx import Namespace, Resource, reqparse, fields, inputs

ns = Namespace('users', description='User related operations')

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='User username')
user_parser.add_argument('email', type=str, help='User email')
user_parser.add_argument('password', type=str, help='User password')
#user_parser.add_argument('include_tokens', type=inputs.boolean, location='args', default=False)

user_model = ns.model('User', {
    'username': fields.String(description='username'),
    'email': fields.String(description='User email'),
    'password': fields.String(description='User password'),
})


@ns.route('/')
class Users(Resource):
    @ns.doc(description='Retrieve all registered users')
    def get(self):
        return {'message': 'You get all users'}

    @ns.doc(description='Register a new user')
    @ns.expect(user_model, validate=True, validate_payload=True)
    def post(self):
        user_data = user_parser.parse_args()
        # Add registration logic here
        return {'message': f'{user_data}'}


@ns.route('/<username>')
class User(Resource):
    @ns.doc(description='Update user details by username')
    @ns.expect(user_model, validate=True, validate_payload=True)
    def put(self, username):
        args = user_parser.parse_args()

        # Add logic to update user details by user_id using args['name'], args['email'], etc.
        # Update the user with the provided data

        return {'message': f'User details updated for user {username}', 'data': args}

    @ns.doc(description='Delete user by username')
    def delete(self, username):
        # Add logic to delete user by user_id
        return {'message': f'User {username} deleted'}

    @ns.doc(description='Get user details by username', params={'include_tokens': {'description': 'Include monitored tokens', 'type': 'boolean', 'default': False}})
    def get(self, username):
        tokens = 'do not include monitored tokens'
        user_parser.add_argument('include_tokens', type=inputs.boolean, location='args', default=False)
        args = user_parser.parse_args()
        include_tokens = args.get('include_tokens', False)

        if include_tokens:
            # Add logic to retrieve user details by user_id and include monitored tokens
            tokens = 'Include monitored tokens'

        # Add logic to retrieve user details by user_id
        return {'message': f'User {username} [{tokens}]'}
