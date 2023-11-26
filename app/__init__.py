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

    return app
