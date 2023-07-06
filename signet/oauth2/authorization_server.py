from authlib.integrations.flask_oauth2 import AuthorizationServer as FlaskAuthorizationServer
from authlib.oauth2.rfc6749 import scope_to_list, InvalidScopeError


def allowed_scopes(supported: list[str], requested: list[str]) -> list[str]:
    # check if requested scope is a subset of scopes_supported
    # if download_file is one of the supported scopes then
    # allow any scope in the request that starts with download_file

    supported = set(supported)
    DL_SCOPE = 'download_file'
    return [s
            for s in requested
            if s in supported or
            (s.startswith(DL_SCOPE) and DL_SCOPE in supported)
            ]


class AuthorizationServer(FlaskAuthorizationServer):
    def validate_requested_scope(self, scope, state=None):
        if len(allowed_scopes(supported=self.scopes_supported, requested=scope_to_list(scope))) == 0:
            raise InvalidScopeError(state=state)
