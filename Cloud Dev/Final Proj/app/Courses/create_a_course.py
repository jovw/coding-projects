from google.cloud import datastore
from flask import current_app, jsonify, request
from ..constants import (
    STATUS_403,
    COURSES,
    USERS,
    STATUS_400)
from ..check_user_role import check_user_role


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + COURSES, methods=['POST'])
    def create_a_course():
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

        # required fields
        required_fields = ['subject',
                           'number',
                           'title',
                           'term',
                           'instructor_id']

        # check if all fields are present
        missing_fields = [
            field for field in required_fields if field not in content]
        if missing_fields:
            return jsonify(STATUS_400), 400

        # get the instructors and store id in list
        client = current_app.client
        query = client.query(kind=USERS)
        query.add_filter('role', '=', 'instructor')
        instructors = list(query.fetch())

        instructor_ids = [instructor.key.id for instructor in instructors]

        # check if the instructor id matched id of instructors
        if content['instructor_id'] not in instructor_ids:
            return jsonify(STATUS_400), 400

        # create the courses
        key = client.key(COURSES)
        course = datastore.Entity(key=key)
        course.update({
            'subject': content['subject'],
            'number': content['number'],
            'title': content['title'],
            'term': content['term'],
            'instructor_id': content['instructor_id'],
        })

        # save the course entity in datastore
        client.put(course)

        # create the self link
        course_id = course.key.id
        self_url = get_base_url() + 'courses/' + str(course_id)

        # return the created course details
        return jsonify({
            'id': course_id,
            'subject': course['subject'],
            'number': course['number'],
            'title': course['title'],
            'term': course['term'],
            'instructor_id': course['instructor_id'],
            'self': self_url
        }), 201
