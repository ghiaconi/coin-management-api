from flask import Flask, jsonify
from config import Config
from flask_migrate import Migrate
from app.models.base import db
from app.routes import blueprint as api_blueprint
from flask_cors import CORS

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(api_blueprint)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models.user import User
    from app.models.token import Token

    return app
