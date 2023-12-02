import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Fetch MySQL connection details from environment variables, otherwise use the defaults
    DB_USER = os.environ.get('DB_USER', 'app')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'app')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'coin_management_api_development')
    RESTX_ERROR_404_HELP = os.environ.get('RESTX_ERROR_404_HELP', False)

    # Construct the MySQL connection string
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Disable tracking modifications of objects and emit signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CoinGecko API
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
    COINGECKO_API_REFRESH_INTERVAL = 60  # seconds. TODO Figure out a good interval for this

    # Excluded attributes for models that implement the serialize() method
    TOKEN_EXCLUDED_ATTRIBUTES = ['id', 'created_at', 'updated_at']
    USER_EXCLUDED_ATTRIBUTES = ['id', 'password', 'created_at', 'updated_at']
