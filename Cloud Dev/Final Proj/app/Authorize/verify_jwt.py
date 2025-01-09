import json
from six.moves.urllib.request import urlopen
from jose import jwt
from flask import jsonify
from ..constants import (
    ALGORITHMS,
    DOMAIN,
    AUDIENCE,
    STATUS_401
)


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def init_app(app):
    """Initialize the app"""
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


def verify_jwt(request):
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization'].split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            raise AuthError(STATUS_401, 401)
        token = auth_header[1]
    else:
        raise AuthError(STATUS_401, 401)

    jsonurl = urlopen(f"https://{DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError(STATUS_401, 401)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break
    if not rsa_key:
        raise AuthError(STATUS_401, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUDIENCE,
            issuer=f"https://{DOMAIN}/"
        )
    except jwt.ExpiredSignatureError:
        raise AuthError(STATUS_401, 401)
    except jwt.JWTClaimsError:
        raise AuthError(STATUS_401, 401)
    except Exception:
        raise AuthError(STATUS_401, 401)

    return payload
