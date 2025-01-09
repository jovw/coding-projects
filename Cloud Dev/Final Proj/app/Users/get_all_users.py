# from google.cloud import datastore
from flask import current_app, jsonify, request
from ..constants import STATUS_403, USERS
from ..check_user_role import check_user_role


def init_app(app):
    @app.route('/' + USERS, methods=['GET'])
    def get_users():
        client = current_app.client

        # check user role
        result = check_user_role(request)

        # Check if role is an error response
        if isinstance(result, tuple) and len(result) == 2:
            return result

        users = result['users']
        user = users[0] if users else None
        role = user['role'] if user else None

        # Get users only if admin
        if role != 'admin':
            return jsonify(STATUS_403), 403

        # Get all the users
        query = client.query(kind=USERS)
        users = list(query.fetch())

        result = []
        for u in users:
            result.append({
                'id': u.key.id,
                'role': u['role'],
                'sub': u['sub']
            })
        return jsonify(result), 200
