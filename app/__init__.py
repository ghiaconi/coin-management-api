from flask import Flask, jsonify
from config import Config
from flask_migrate import Migrate
from app.models.base import db
from app.routes import blueprint as api_blueprint

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models.user import User
    from app.models.token import Token

    @app.route('/test/', methods=['GET'])
    def test_page():
        last_user = User.query.order_by(User.id.desc()).first()
        last_token = Token.query.order_by(Token.id.desc()).first()
        return jsonify({'message': 'Hello World!',
                        'user': str(vars(last_user)),
                        'token': str(vars(last_token))
                        })

    return app
