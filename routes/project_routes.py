import json
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, redirect, make_response
from middlewares.user_middlewares import require_student, require_login
from mongo import database
from github import git_request

projects = Blueprint('projects', __name__)


@projects.route("/projects")
def project():
    student = require_student(request.cookies, redirect)

    if student:

        # run below if the git_username is not set
        if not student['git_username']:
            return redirect("/user/setup_github")

        git_projects = git_request(f"/users/{student['git_username']}/repos")

        def essentials(data):
            return {
                'id': data['id'],
                'name': data['name'],
                'html_url': data['html_url'],
                'homepage': data['homepage'],
                'description': data['description'],
                'language': data['language'],
                'avatar_url': data['owner']['avatar_url'],
                'updated_at': datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
            }

        git_projects = list(map(essentials, git_projects))
        git_projects.sort(key=lambda r: r['updated_at'], reverse=True)

        return render_template('view/projects.html', user_auth=student, git_projects=git_projects)


@projects.route("/projects/<repo>", methods=['GET', 'POST'])
def project_repo(repo):
    user = require_login(request.cookies)

    if user:
        # fetch the repository requested
        repository = git_request(f"/repos/{user['git_username']}/{repo}")

        # fetch the languages used for this repository
        # required in order to draw the chart
        repo_stack = git_request('/repos/%s/%s/languages' % (user['git_username'], repo))

        # gets the languages which this repository consist and get the percentage.
        repo_stack_sum = sum([value for key, value in repo_stack.items()])

        data = {
            'id': repository['id'],
            '_user': user['user_name'],
            'name': repo,
            'stack_labels': list(repo_stack),
            'stack_value': [round((value / repo_stack_sum) * 100, 0) for key, value in repo_stack.items()],
            'description': repository['description'],
            'updated_at': datetime.strptime(repository['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
            'homepage': repository['homepage'],
            'html_url': repository['html_url'],
            'language': repository['language'],

        }
        if request.method == 'POST':
            if not database.create_post(data):

                return "post already exist"

            return redirect("/posts")
        return render_template('view/project_single.html', referrer=request.referrer, user_auth=user, project=data)
