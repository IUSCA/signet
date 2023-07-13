from authlib.integrations.sqla_oauth2 import create_query_client_func, create_revocation_endpoint, \
    create_query_token_func
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7523 import JWTBearerTokenGenerator

from signet.models import db, OAuth2Token, OAuth2Client
from signet.oauth2.authorization_server import AuthorizationServer


def create_save_token_func(session, token_model):
    """Create an ``save_token`` function that can be used in authorization
    server.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """

    def save_token(token, request):
        client = request.client
        item = token_model(
            client_id=client.client_id,
            **token
        )
        session.add(item)
        session.commit()

    return save_token


query_client = create_query_client_func(db.session, OAuth2Client)
save_token = create_save_token_func(db.session, OAuth2Token)
query_token = create_query_token_func(db.session, OAuth2Token)

authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)


def config_oauth(app):
    authorization.init_app(app)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_token_generator(grants.ClientCredentialsGrant.GRANT_TYPE, create_token_generator())

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # support introspection


def create_token_generator():
    with open('keys/auth.key', 'r') as f:
        secret_key = f.read()

    jwtBearerTokenGenerator = JWTBearerTokenGenerator(secret_key=secret_key, issuer='signet.sca.iu.edu')

    def token_generator(grant_type, client, user=None, scope=None, expires_in=None, include_refresh_token=True):
        if not expires_in:
            client_scopes = client.scope.split(' ')
            expires_in = 24 * 60 * 60 if 'download_file' in client_scopes else 864000

        return jwtBearerTokenGenerator.generate(grant_type, client, user, scope, expires_in)

    return token_generator
