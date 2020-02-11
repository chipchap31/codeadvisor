import json
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, redirect, make_response
from middlewares.user_middlewares import require_login
from mongo import database
from github import git_request

users = Blueprint('users', __name__)


@users.route("/projects/new", methods=["POST", "GET"])
def project_new():
    user = require_login(request.cookies)

    if user:  # check if user is logged in

        if user["role"] == "student":  # check if user is logged in as student

            if request.method == 'POST':

                if not user['git_username']:  # true if github username is not set yet
                    user['git_username'] = request.form['git_username']

                    res = make_response(redirect('/projects/new'))
                    if database.set_git_username(user['user_name'], request.form['git_username']):
                        res.set_cookie('user_data', json.dumps(user))
                        return res
                    else:
                        print("Cannot set git_username")

                # if github user name is not set the block of code below will not run
                if database.create_project(request.form, user['user_name']):
                    return redirect("/projects")
                return render_template("view/project_new.html", user_auth=user)

            if not user['git_username']:
                return render_template("view/git_username.html", user_auth=user)

            # render all of the user's repositories
            projects = git_request(f"/users/{user['git_username']}/repos")

            def essentials(data):
                return {
                    'name': data['name'],
                    'html': data['html_url'],
                    'homepage': data['homepage'],
                    'description': data['description'],
                    'language': data['language'],
                    'avatar_url': data['owner']['avatar_url'],
                    'created_at': datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                    'updated_at': datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
                }

            projects_formatted = list(map(essentials, projects))

            return render_template("view/project_new.html", user_auth=user, project_list=projects_formatted)


@users.route('/projects/delete/<id>')
def delete_project(id):
    if require_login(request.cookies):
        database.project_delete(id)
    return redirect('/projects')


@users.route("/users/set_git_username")
def set_git_username():
    user = require_login(request.cookies)
    if user:
        return render_template('view/git_username.html', user_auth=user)
