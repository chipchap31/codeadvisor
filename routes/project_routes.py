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
    user = require_login(request.cookies)
    # render login form if not login
    if not user:
        return redirect('/login')

    # check if the github username is provided
    if not user['git_username']:
        render_template('projects/projects_setup.html', user_auth=user)

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

    # make a request to github api that returns the repositories of the username provide

    git_projects = git_request(f"/users/{user['git_username']}/repos")
    project_len = len(git_projects)
    # get page number from the path
    page = int(request.args.get('page')) if request.args.get('page') else 1

    # if the variable page does not exist
    # limit the projects rendered to five
    if request.args.get('page'):
        git_projects = list(map(essentials, git_projects))[
            (5 * page) - 5:((5 * page) - 5) * 2]
    else:
        git_projects = list(map(essentials, git_projects))[:5]

    # arrange the list depending on the updated date
    git_projects.sort(key=lambda r: r['updated_at'], reverse=True)

    return render_template('projects/projects.html', config={
        'curr_page': page + 1,
        'ref': request.referrer,
        'projects': git_projects,
        'render_next': (page * 5) + len(git_projects) - 5 < project_len
    }, user_auth=user)


@projects.route("/projects/<repo>", methods=['GET', 'POST'])
def project_repo(repo):
    user = require_login(request.cookies)

    if not user:
        return redirect('/login')
    # fetch the repository requested
    repository = git_request(f"/repos/{user['git_username']}/{repo}")

    # fetch the languages used for this repository
    # required in order to draw the chart
    repo_stack = git_request('/repos/%s/%s/languages' %
                             (user['git_username'], repo))

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

    # checks if the method is post and the
    if not database.create_post(data) and request.method == 'POST':
        return redirect('/posts')

    return render_template('projects/project_single.html', referrer=request.referrer, user_auth=user, project=data)


@projects.route("/projects/load")
def project_load():
    return {"message": 'hello world'}
