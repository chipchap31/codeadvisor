from flask import Blueprint, redirect, request, abort, render_template

from middlewares.user_middlewares import require_login
from mongo import database
from datetime import datetime
import ast
posts = Blueprint('posts', __name__)


@posts.route('/posts')
def post_fetch():
    """ Get all the of the posts """
    user = require_login(request.cookies)

    if not user:
        return abort(401)

    posts = database.post_fetch(
        user=user['user_name'], sort=request.args.get('sort') or 'posted_at')

    posts_len = len(posts)
    # get current page
    curr_page = int(request.args.get('page')
                    ) if request.args.get('page') else 1

    if curr_page == 1:
        posts_limit = posts[:5]

    else:
        posts_limit = posts[(5 * curr_page) - 5: ((5 * curr_page) - 5) * 2]

    return render_template('posts/posts.html', user_auth=user, config={
        'posts': posts_limit,
        'posts_len': posts_len,
        'pagination': round(posts_len / 5) + 2,
        'curr_page': curr_page,
        'ref': request.referrer,
        'curr_sort': request.args.get('sort') or 'posted_at',
        'render_next': (curr_page * 5) + len(posts_limit) - 5 < posts_len,

    })


@posts.route('/posts/delete')
def post_delete():
    if not database.data_delete({
        'collection': 'posts',
        '_id': int(request.args.get('id')),
        '_user': request.args.get('user')
    }):
        return abort(500)

    return redirect('/posts')


@posts.route('/posts/<name>', methods=["GET", "POST"])
def repository_view(name):
    user = require_login(request.cookies)

    if not user:
        return abort(401)

    if request.method == "POST":
        data = request.form
        labels = ast.literal_eval(request.form.get('labels'))
        doc, feedback_arr = {}, []
        index = 1

        # we loop through the labels and using the variable index
        # we can point the corresponding rate and description from the form

        for label in labels:
            feedback_arr.append({
                label: {
                    "rate": int(data['rate%s' % index]),
                    "advice": data['advice%s' % index]
                }

            })
            index += 1

        doc = {
            'feedback': feedback_arr,
            'post_name': data['name'],
            'post_id': int(data['id']),
            '_user': user['_id'],
            '_username': user['user_name'],
            'posted_at': datetime.now(),
            'like': [],
            'dislike': []
        }

        if not database.create_feedback(doc):
            return render_template('posts/post_single.html',
                                   user_auth=user, feedback_error=True, post=database.post_fetch(name=name, user=user['user_name']))

        return redirect('/posts/' + name)

    # get the feedback for this posts

    feedbacks = list(database.feedback_fetch({'post_name': name}))

    return render_template('posts/post_single.html',
                           user_auth=user,
                           referrer=request.referrer, post=database.post_fetch(
                               name=name, user=user['user_name']), feedbacks=feedbacks)


@posts.route('/posts/<feedback_id>/<impression>', methods=["POST"])
def feedback_option(feedback_id, impression):
    user = require_login(request.cookies)

    if not user:
        return abort(401)
    database.feedback_impression({
        '_user': user['_id'],
        '_id': feedback_id,
        'impression': impression
    })
    return {}
