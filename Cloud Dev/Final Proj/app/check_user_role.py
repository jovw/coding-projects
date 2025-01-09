# from google.cloud import datastore
from flask import current_app, jsonify
from .Authorize.verify_jwt import verify_jwt, AuthError
from .constants import STATUS_404, USERS


def check_user_role(request):
    """
    chekc the user's role and verify that user is valid
    """
    try:
        # Verify user and get sub
        payload = verify_jwt(request)
    except AuthError as e:
        return jsonify(e.error), e.status_code

    sub = payload['sub']

    # Get the logged-in user from datastore
    client = current_app.client
    query = client.query(kind=USERS)
    query.add_filter('sub', '=', sub)
    users = list(query.fetch())

    if not users:
        return jsonify(STATUS_404), 404

    return {'users': users, 'sub': sub}
