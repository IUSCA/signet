from authlib.integrations.sqla_oauth2 import create_query_client_func, create_revocation_endpoint, \
    create_query_token_func
from authlib.oauth2.rfc6749 import grants

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

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # support introspection
