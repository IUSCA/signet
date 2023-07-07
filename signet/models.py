from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2TokenMixin
from authlib.oauth2.rfc6749 import scope_to_list, list_to_scope
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Text

from signet.oauth2.authorization_server import allowed_scopes

db = SQLAlchemy()


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'
    id = db.Column(db.Integer, primary_key=True)

    def get_allowed_scope(self, scope):
        if not scope:
            return ''

        return list_to_scope(
            allowed_scopes(
                supported=self.scope.split(),
                requested=scope_to_list(scope)
            )
        )


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'
    id = db.Column(db.Integer, primary_key=True)
    access_token = Column(Text, unique=True, nullable=False)

    def is_refresh_token_active(self):
        pass
