import json
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, redirect, make_response
from middlewares.user_middlewares import require_login
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
    # fetch all github projects
    try:
        projects = list(map(essentials, git_request(
            f"/users/{user['git_username']}/repos")))
    except:
        projects = []

        # this is the number of the public repos of the current user
    projects_len = len(projects)

    curr_page = int(request.args.get('page')
                    ) if request.args.get('page') else 1

    if curr_page == 1:
        project_limit = projects[:5]
    else:
        project_limit = projects[(5 * curr_page) -
                                 5: ((5 * curr_page) - 5) * 2]

    top_advisors = database.get_top_advisor()

    return render_template('projects/projects.html', user_auth=user, config={
        "projects": project_limit,
        "projects_len": projects_len,
        "pagination": round(projects_len / 5) + 1,
        'curr_page': curr_page,
        'ref': request.referrer,
        'curr_sort': request.args.get('sort') or 'posted_at',
        'render_next': (curr_page * 5) + len(project_limit) - 5 < projects_len,
        "top_advisors": top_advisors
    })


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
    if request.method == 'POST':
        database.create_post(data)
        return redirect('/posts')

    top_advisors = database.get_top_advisor()

    return render_template('projects/project_single.html',
                           config={
                               "top_advisors": database.get_top_advisor()
                           },
                           referrer=request.referrer, user_auth=user, project=data)
