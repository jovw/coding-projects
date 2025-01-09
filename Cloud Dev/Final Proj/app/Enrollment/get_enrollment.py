from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    STATUS_404,
    COURSES,
    USERS,
    ENROLLMENTS
)
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + COURSES + '/<int:course_id>/students', methods=['GET'])
    def get_enrollment(course_id):
        # Check user role
        result = check_user_role(request)

        # Check if result is an error response
        if isinstance(result, tuple) and len(result) == 2:
            return result

        # Extract users and sub
        users = result['users']
        user = users[0] if users else None
        role = user['role'] if user else None
        user_sub = user['sub'] if user else None

        client = current_app.client

        # If course does not exist, return 404
        course = client.get(key=client.key(COURSES, course_id))

        if not course:
            return jsonify(STATUS_403), 403

        # Check if user is an admin or the instructor of the course
        if role != 'admin':
            query = client.query(kind=USERS)
            query.add_filter('sub', '=', user_sub)
            instructor = list(query.fetch())

            if not instructor or instructor[0].key.id != course.get('instructor_id'):
                return jsonify(STATUS_403), 403

        # Get enrollments
        query = client.query(kind=ENROLLMENTS)
        query.add_filter('course_id', '=', course_id)
        enrollments = list(query.fetch())

        student_ids = [enrollment['student_id'] for enrollment in enrollments]

        # Return the list of student IDs
        return jsonify(student_ids), 200
