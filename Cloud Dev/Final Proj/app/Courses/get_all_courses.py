from flask import current_app, jsonify, request
from ..constants import COURSES


def get_base_url():
    """Returns the base URL derived from the current request."""
    return request.host_url


def init_app(app):
    @app.route('/' + COURSES, methods=['GET'])
    def get_all_courses():
        """Returns all courses."""
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', 3, type=int)

        client = current_app.client
        query = client.query(kind=COURSES)
        query.order = ['subject']
        courses = list(query.fetch(limit=limit, offset=offset))

        for c in courses:
            c['id'] = c.key.id
            c['self'] = get_base_url() + 'courses/' + str(c.key.id)

        if courses:
            next_offset = offset + limit
            next_url = f"{get_base_url()}courses?offset={next_offset}&limit={limit}"
        else:
            next_url = None

        response = {
            "courses": courses,
            "next": next_url
        }

        return jsonify(response)