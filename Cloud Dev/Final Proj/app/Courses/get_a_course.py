from flask import current_app, jsonify, request
from ..constants import (
    COURSES,
    STATUS_404)


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + COURSES + '/<int:course_id>', methods=['GET'])
    def get_a_courses(course_id):
        """Returns all courses."""
        client = current_app.client
        course = client.get(key=client.key(COURSES, course_id))

        if not course:
            return jsonify(STATUS_404), 404

        course['id'] = course_id
        course['self'] = get_base_url() + 'courses/' + str(course_id)
        return jsonify(course), 200
