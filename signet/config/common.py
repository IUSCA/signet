import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']

config = {
    'database': {
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "hostname": "localhost",
        "port": "5532",
        "dbname": POSTGRES_DB,
        "dialect": "postgresql+psycopg2",
    },
}
