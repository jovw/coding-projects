from flask import Flask, current_app
from google.cloud import datastore
from .Authorize import authorize_user
from .Users import (
    get_all_users,
    create_update_avatar,
    get_user_avatar,
    delete_user_avatar,
    get_a_user
    )
from .Courses import (
    create_a_course,
    get_all_courses,
    get_a_course,
    update_a_course,
    delete_a_course
    )
from .Enrollment import update_enrollment, get_enrollment


def create_app():
    app = Flask(__name__)
    init_client(app)

    authorize_user.init_app(app)

    get_all_users.init_app(app)
    get_a_user.init_app(app)
    create_update_avatar.init_app(app)
    get_user_avatar.init_app(app)
    delete_user_avatar.init_app(app)

    create_a_course.init_app(app)
    get_all_courses.init_app(app)
    get_a_course.init_app(app)
    update_a_course.init_app(app)
    delete_a_course.init_app(app)

    update_enrollment.init_app(app)
    get_enrollment.init_app(app)

    return app


def init_client(app):
    with app.app_context():
        current_app.client = datastore.Client(project='hw6-vanwykj')
