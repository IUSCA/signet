import urllib.parse

from signet.app import create_app
from signet.config import config

store = config['database']
conn_string = f"{store['dialect']}://{store['user']}:{urllib.parse.quote(store['password'])}@{store['hostname']}:{store['port']}/{store['dbname']}"

app = create_app({
    'SQLALCHEMY_DATABASE_URI': conn_string,
    'OAUTH2_SCOPES_SUPPORTED': ['microservice', 'download_file', 'upload_file']
})
