from google.cloud import storage
from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    PHOTO_BUCKET,
    USERS,
    COURSES,
    ENROLLMENTS
)
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def get_user_courses(client, user_id, role):
    courses = []
    if role == 'instructor':
        query = client.query(kind=COURSES)
        query.add_filter('instructor_id', '=', user_id)
        courses = list(query.fetch())
    elif role == 'student':
        query = client.query(kind=ENROLLMENTS)
        query.add_filter('student_id', '=', user_id)
        enrollments = list(query.fetch())
        courses = [client.get(key=client.key(COURSES, enrollment[
            'course_id'])) for enrollment in enrollments]

    return [get_base_url() + 'courses/' + str(
        course.key.id) for course in courses if course]


def get_avatar_url(user_id):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(PHOTO_BUCKET)
    blobs = list(bucket.list_blobs(prefix=f'avatars/{user_id}/'))

    if blobs:
        return get_base_url() + USERS + f'/{user_id}/avatar'
    return None


def init_app(app):
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        # Check user role
        result = check_user_role(request)
        if isinstance(result, tuple) and len(result) == 2:
            return result

        users = result['users']
        requesting_user = users[0] if users else None
        role = requesting_user['role'] if requesting_user else None
        user_sub = requesting_user['sub'] if requesting_user else None

        client = current_app.client

        # Get the requested user
        user = client.get(key=client.key(USERS, user_id))
        if not user:
            return jsonify(STATUS_403), 403

        # Check if user has permission
        if role != 'admin' and user['sub'] != user_sub:
            return jsonify(STATUS_403), 403

        # Build the response
        response_data = {
            'id': user.key.id,
            'role': user['role'],
            'sub': user['sub']
        }

        # Include avatar_url if the user has an avatar
        avatar_url = get_avatar_url(user.key.id)
        if avatar_url:
            response_data['avatar_url'] = avatar_url

        # Include courses if the user is an instructor or student
        if user['role'] in ['instructor', 'student']:
            response_data['courses'] = get_user_courses(
                client, user.key.id, user['role'])

        return jsonify(response_data), 200
