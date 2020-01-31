from flask import Blueprint, render_template, request, make_response, redirect
from middlewares.user_middlewares import require_login
from mongo import database
projects = Blueprint('projects', __name__)


@projects.route("/projects/new", methods=["POST", "GET"])
def project_new():
    user = require_login(request.cookies)

    if user:  # check if user is logged in

        if user["role"] == "student":  # check if user is logged in as student

            if request.method == 'POST':
                if database.create_project(request.form):
                    return render_template("student/projects.html")
                return render_template("student/project_new.html", user_auth=user)

            return render_template("student/project_new.html", user_auth=user)
