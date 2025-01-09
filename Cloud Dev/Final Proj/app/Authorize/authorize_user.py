from flask import Flask, request, jsonify
import requests
from authlib.integrations.flask_client import OAuth
from ..constants import (
    STATUS_400,
    STATUS_401,
    CLIENT_ID,
    CLIENT_SECRET,
    DOMAIN,
    AUDIENCE
)

app = Flask(__name__)


def init_app(app):
    oauth = OAuth(app)

    oauth.register(
        'auth0',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        api_base_url='https://' + DOMAIN,
        access_token_url='https://' + DOMAIN + '/oauth/token',
        authorize_url='https://' + DOMAIN + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    @app.route('/users/login', methods=['POST'])
    def login_user():
        content = request.get_json()
        print(content)  # Debugging line to verify the request payload
        if (
            not content or
            not all(key in content for key in ('username', 'password'))
        ):
            return jsonify(STATUS_400), 400

        username = content["username"]
        password = content["password"]
        body = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'audience': AUDIENCE
        }
        headers = {'Content-Type': 'application/json'}
        url = 'https://' + DOMAIN + '/oauth/token'
        r = requests.post(url, json=body, headers=headers)

        if r.status_code != 200:
            return jsonify(STATUS_401), 401

        token = r.json().get('access_token')
        return jsonify({"token": token}), 200
