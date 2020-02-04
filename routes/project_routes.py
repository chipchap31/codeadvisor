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
                if database.create_project(request.form, user['user_name']):
                    return redirect("/projects")
                return render_template("student/project_new.html", user_auth=user)

            return render_template("student/project_new.html", user_auth=user)


@projects.route("/projects")
def project():
    user = require_login(request.cookies)
    if user:
        if user['role'] == 'student':




            if request.args.get('sort'):
                return render_template('student/projects.html', projects=database.fetch_projects({
                "user": user['user_name'],
                "sort": request.args.get('sort'),
                "limit": request.args.get("limit")
                }), user_auth=user)




            return render_template('student/projects.html', projects=database.fetch_projects({
            "user": user['user_name'],
            "sort": request.args.get('sort'),
            "limit": request.args.get("limit")
            }), user_auth=user)





@projects.route("/projects/<id>")
def single_project(id):
    user = require_login(request.cookies)
    if user:

        return render_template("student/project_single.html",user_auth=user, project=database.project_single(id, user["_id"]))

@projects.route('/projects/delete/<id>')
def delete_project(id):
    if require_login(request.cookies):

        database.project_delete(id)
    return redirect('/projects')
