from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    COURSES,
    ENROLLMENTS,
)
from ..check_user_role import check_user_role


def init_app(app):
    @app.route('/' + COURSES + '/<int:course_id>', methods=['DELETE'])
    def delete_a_course(course_id):
        # Check user role
        result = check_user_role(request)

        # Check if result is an error response
        if isinstance(result, tuple) and len(result) == 2:
            return result

        # Extract users and sub
        users = result['users']
        user = users[0] if users else None
        role = user['role'] if user else None

        # Get users only if admin
        if role != 'admin':
            return jsonify(STATUS_403), 403

        # If course does not exist, return 404
        client = current_app.client
        course = client.get(key=client.key(COURSES, course_id))

        if not course:
            return jsonify(STATUS_403), 403

        # Delete the course
        client.delete(course.key)

        # Delete enrollments associated with the course
        query = client.query(kind=ENROLLMENTS)
        query.add_filter('course_id', '=', course_id)
        enrollments = list(query.fetch())

        for enrollment in enrollments:
            client.delete(enrollment.key)

        # Return no content
        return '', 204
