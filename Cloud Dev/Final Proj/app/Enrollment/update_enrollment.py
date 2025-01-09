from google.cloud import datastore
from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    STATUS_409,
    COURSES,
    USERS,
    ENROLLMENTS
)
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + COURSES + '/<int:course_id>/students', methods=['PATCH'])
    def update_enrollment(course_id):
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

        # If user is not admin or instructor of this course, return 403
        client = current_app.client
        course = client.get(key=client.key(COURSES, course_id))

        if not course:
            return jsonify(STATUS_403), 403

        # Check if user is an admin or the instructor of the course
        if role != 'admin':
            query = client.query(kind=USERS)
            query.add_filter('sub', '=', user_sub)
            instructor = list(query.fetch())

            print(instructor[0].key.id)
            print(course.get('instructor_id'))

            if not instructor or instructor[0].key.id != course.get('instructor_id'):
                return jsonify(STATUS_403), 403

        # Get content
        try:
            content = request.get_json()
        except Exception:
            return jsonify({"Error": "Invalid JSON format"}), 400

        add = content.get('add', [])
        remove = content.get('remove', [])

        # Validate enrollment data
        if set(add) & set(remove):
            return jsonify(STATUS_409), 409

        query = client.query(kind=USERS)
        query.add_filter('role', '=', 'student')
        students = list(query.fetch())
        student_ids = {student.key.id for student in students}

        if not set(add).issubset(student_ids) or not set(remove).issubset(student_ids):
            return jsonify(STATUS_409), 409

        # Update enrollments
        query = client.query(kind=ENROLLMENTS)
        query.add_filter('course_id', '=', course_id)
        current_enrollments = {enrollment['student_id']: enrollment.key for enrollment in query.fetch()}

        for student_id in add:
            if student_id not in current_enrollments:
                enrollment_key = client.key(ENROLLMENTS)
                enrollment = datastore.Entity(key=enrollment_key)
                enrollment.update({
                    'course_id': course_id,
                    'student_id': student_id
                })
                client.put(enrollment)

        for student_id in remove:
            if student_id in current_enrollments:
                client.delete(current_enrollments[student_id])

        # Return no content
        return '', 200
