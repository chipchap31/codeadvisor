from flask import Blueprint, render_template, request, make_response, redirect
from middlewares.user_middlewares import require_login

projects = Blueprint('projects', __name__)


@projects.route("/projects/new"):
def project_new():
    user = require_login(request.cookies)

    if user:
        if user["role"] == student:
            return render_template("student/")
