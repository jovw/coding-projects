from google.cloud import storage
from flask import current_app, jsonify, request, send_file
import io
from ..constants import (
    STATUS_403,
    STATUS_404,
    USERS,
    PHOTO_BUCKET
    )
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + USERS + '/<int:user_id>/avatar', methods=['GET'])
    def get_user_avatar(user_id):

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
        if user['sub'] != sub:
            return jsonify(STATUS_403), 403

        # get avatar
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(PHOTO_BUCKET)
        blobs = list(bucket.list_blobs(prefix=f'avatars/{user_id}/'))

        # return 404 if not found
        if not blobs:
            return jsonify(STATUS_404), 404

        # if there is just one avatar
        blob = blobs[0]
        file_obj = io.BytesIO()
        blob.download_to_file(file_obj)
        file_obj.seek(0)

        return send_file(file_obj,
                         mimetype='image/png',
                         download_name=blob.name.split('/')[-1])
