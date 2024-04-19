import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
ISSUER = os.environ['ISSUER']

config = {
    'database': {
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "hostname": POSTGRES_HOST,
        "port": POSTGRES_PORT,
        "dbname": POSTGRES_DB,
        "dialect": "postgresql+psycopg2",
    },
    'issuer': ISSUER,
    'token_expiration': {
        'download_file': 30,
        'upload_file': 30,
        'fs_read': 5 * 60,
        'default': 864000
    }
}
