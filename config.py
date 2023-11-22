import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Fetch MySQL connection details from environment variables, otherwise use the defaults
    DB_USER = os.environ.get('DB_USER', 'app')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'app')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'coin_management_api_development')

    # Construct the MySQL connection string
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Disable tracking modifications of objects and emit signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # You can then use this configuration in your Flask app
    # app.config.from_object(Config)
