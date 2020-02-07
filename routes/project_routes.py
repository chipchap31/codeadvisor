import json
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, redirect, make_response
from middlewares.user_middlewares import require_student
from mongo import database
from github import git_request

projects = Blueprint('projects', __name__)


@projects.route("/projects")
def project():
    student = require_student(request.cookies, redirect)
    print(student)
    if student:

        # run below if the git_usernae is not set
        if not student['git_username']:
            return redirect("/user/setup_github")
        
        git_projects = git_request(f"/users/{student['git_username']}/repos")

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

        git_projects = list(map(essentials, git_projects))

        return render_template('view/projects.html', user_auth=student, git_projects=git_projects)

















       