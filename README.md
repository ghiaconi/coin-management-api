# CoinManagementAPI

CoinManagementAPI is a Flask-based RESTful API for managing cryptocurrency data, user information, and token-related functionalities.

## Getting Started

These instructions will guide you through setting up the project on your local machine.

### Prerequisites

- Python (version X.X.X)
- Flask-SQLAlchemy
- MySQL database

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

**Apply database migrations:**

    ```bash
    flask db upgrade
    ```

### Running the Application

Run the following command to start the Flask development server:

   ```bash
   flask run
   ```
 ### Swagger Documentation
    Swagger documentation can be found at http://localhost:5000/docs