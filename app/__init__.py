from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models.user import User
    from app.models.token import Token

    @app.route('/test/', methods=['GET'])
    def test_page():
        return jsonify({'message': 'Hello World!'})

    return app
