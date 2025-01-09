from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    COURSES,
    STATUS_400,
    USERS)
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + COURSES + '/<int:course_id>', methods=['PATCH'])
    def update_a_course(course_id):
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

        # get content
        try:
            content = request.get_json()
        except Exception:
            return jsonify({"Error": "Invalid JSON format"}), 400

        # if course does not exist, return 404
        client = current_app.client
        course = client.get(key=client.key(COURSES, course_id))

        if not course:
            return jsonify(STATUS_403), 403

        # Validate instructor_id if present in the request
        if 'instructor_id' in content:
            query = client.query(kind=USERS)
            query.add_filter('role', '=', 'instructor')
            instructors = list(query.fetch())
            instructor_ids = [instructor.key.id for instructor in instructors]

            if content['instructor_id'] not in instructor_ids:
                return jsonify(STATUS_400), 400

        # Update the course with the provided fields
        for field in ['subject', 'number', 'title', 'term', 'instructor_id']:
            if field in content:
                course[field] = content[field]

        # Save the updated course entity in datastore
        client.put(course)

        # Create the self link
        course_id = course.key.id
        self_url = get_base_url() + 'courses/' + str(course_id)

        # Return the updated course details
        return jsonify({
            'id': course_id,
            'subject': course.get('subject'),
            'number': course.get('number'),
            'title': course.get('title'),
            'term': course.get('term'),
            'instructor_id': course.get('instructor_id'),
            'self': self_url
        }), 200
