from flask import Blueprint, redirect, request, abort, render_template

from middlewares.user_middlewares import require_login
from mongo import database

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def post_fetch():
    """ Get all the of the posts """
    user = require_login(request.cookies)

    if not user:
        return abort(401)

    return render_template('posts/posts.html', user_auth=user, posts=database.post_fetch(user=user['user_name']))


@posts.route('/posts/delete')
def post_delete():
    if not database.data_delete({
        'collection': 'posts',
        '_id': int(request.args.get('id')),
        '_user': request.args.get('user')
    }):
        return abort(500)

    return redirect('/posts')


@posts.route('/posts/<name>')
def repository_view(name):
    user = require_login(request.cookies)

    if not user:
        return abort(401)

    return render_template('posts/post_single.html', user_auth=user, referrer=request.referrer, post=database.post_fetch(
        name=name, user=user['user_name']))
