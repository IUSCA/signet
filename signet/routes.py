import time

from authlib.jose import JsonWebKey
from flask import Blueprint, request, jsonify
from werkzeug.security import gen_salt

from signet.models import OAuth2Client, db
from signet.oauth2_server import authorization

bp = Blueprint('home', __name__)


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

@bp.route('/health', methods=['GET'])
def health():
    return 'OK'

@bp.route('/create_client', methods=['POST'])
def create_client():
    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    # noinspection PyArgumentList
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form.get("client_uri"),
        "grant_types": split_by_crlf(form.get("grant_type", "")),
        "redirect_uris": split_by_crlf(form.get("redirect_uri", "")),
        "response_types": split_by_crlf(form.get("response_type", "")),
        "scope": form["scope"],
        "token_endpoint_auth_method": form.get("token_endpoint_auth_method")
    }
    client.set_client_metadata(client_metadata)

    if form.get('token_endpoint_auth_method') is None:
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()

    return jsonify(client.client_info)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


# @bp.route('/oauth/introspect', methods=['POST'])
# def introspect_token():
#     return authorization.create_endpoint_response(MyIntrospectionEndpoint.ENDPOINT_NAME)


@bp.route('/oauth/jwks', methods=['GET'])
def jwks():
    with open('keys/auth.pub', 'r') as f:
        public_key_str = f.read()
        public_key = JsonWebKey.import_key(public_key_str)
        return jsonify({
            'keys': [public_key.as_dict()]
        })
