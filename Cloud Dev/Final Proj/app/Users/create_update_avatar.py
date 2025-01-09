from google.cloud import storage
from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    STATUS_400,
    USERS,
    PHOTO_BUCKET
    )
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + USERS + '/<int:user_id>/avatar', methods=['POST'])
    def create_update_avatar(user_id):
        if 'file' not in request.files:
            return jsonify(STATUS_400), 400

        # Check user role
        result = check_user_role(request)

        # Check if result is an error response
        if isinstance(result, tuple) and len(result) == 2:
            return result

        # Extract users and role
        sub = result['sub']

        # get the user_id information
        client = current_app.client
        user = client.get(key=client.key(USERS, user_id))

        # if the user requesting does not equal the user signed in
        if user is None or user['sub'] != sub:
            return jsonify(STATUS_403), 403

        file_obj = request.files['file']
        if not file_obj.filename.endswith('.png'):
            return jsonify({"error": "File must be a .png"}), 400

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(PHOTO_BUCKET)
        blob = bucket.blob(f'avatars/{user_id}/avatar.png')
        file_obj.seek(0)
        blob.upload_from_file(file_obj)

        avatar_url = f'{get_base_url()}users/{user_id}/avatar'

        return jsonify({
            "avatar_url": avatar_url
        }), 200
