from authlib.common.security import generate_token
from authlib.integrations.sqla_oauth2 import create_query_client_func, create_revocation_endpoint, \
    create_query_token_func
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6750 import BearerTokenGenerator

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
    def token_generator(*args, **kwargs):
        return generate_token(length=42)

    def expires_generator(client, grant_type):
        client_scopes = client.scope.split(' ')
        if 'download_file' in client_scopes:
            return 30
        else:
            return 864000

    return BearerTokenGenerator(
        access_token_generator=token_generator,
        refresh_token_generator=None,
        expires_generator=expires_generator
    )
