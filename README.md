# CoinManagementAPI

CoinManagementAPI is a Flask-based REST API for managing cryptocurrency data, user information, and token-related functionalities.
It uses the [CoinGecko API](https://www.coingecko.com/en/api) to fetch and store cryptocurrency data.
The cache mechanism is not yet implemented, so the API will not re-fetch the data from the CoinGecko API every time a request is made.
Only when creating tokens not existing then the coin data is asked from the CoinGecko API.

## Getting Started

These instructions will guide you through setting up the project on your local machine.

### Prerequisites

- Python
- Flask-SQLAlchemy
- MySQL database 
- Flask-Migrate
- Flask-RESTx
- Flask-CORS


Check the [requirements.txt](requirements.txt) file for more details

### Run bare metal

**Install dependencies:**

    pip install -r requirements.txt

Do not forget to sync your dependencies after installing new packages:

    pip freeze > requirements.txt

Set at least the following environment variables:

    - `FLASK_ENV`=development
    - `SECRET_KEY`: Flask secret key
    - `DB_USER`: MySQL database user
    - `DB_PASSWORD`: MySQL database password
    - `DB_HOST`: MySQL database host (default: `127.0.0.1`)
    - `DB_PORT`: MySQL database port (default: `3306`)
    - `DB_NAME`: MySQL database name (default: `coin_management_api_development`)

**Database**

The database is managed using Flask-Migrate. It does not support creating a database only migration, so you have to connect to your MySql server and create the database manually.
    
    mysql -h localhost -P 3306 -u app --protocol=tcp -p

    mysql> CREATE DATABASE coin_management_api_development;

Then create the table and run the migrations:

    flask db upgrade

### Running the Application

Run the following command to start the Flask development server:

   flask run

 ### Swagger Documentation
    Swagger documentation can be found at http://localhost:5000