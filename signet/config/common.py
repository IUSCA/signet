import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
DB_PASSWORD = os.environ['DB_PASSWORD']

config = {
    'database': {
        "user": "appuser",
        "password": DB_PASSWORD,
        "hostname": "localhost",
        "port": "5532",
        "dbname": "app",
        "dialect": "postgresql+psycopg2",
    },
}
