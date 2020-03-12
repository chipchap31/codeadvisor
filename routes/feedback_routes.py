from flask import Blueprint, redirect, request, abort, render_template

from middlewares.user_middlewares import require_login
from mongo import database

feedback = Blueprint('feedback', __name__)


@feedback.route('/feedback/new', methods=['POST'])
def feedback_new():
    # allow this function if the user's role is equal to "advisor"
    # call the function create_feedback mongo
    # if not redirect to an error page

    user = require_login(request.cookies)

    if not user:
        return abort(401)

    data = {
        "_user": user['_id'],
        "form": request.form
    }

    if not database.create_feedback(data):
        return abort(500)

    # get the project title from the form

    return redirect("/posts")


@feedback.route('/feedback/delete/<id>')
def delete_feedback(id):
    deleted = database.delete_feedback(id)

    if not deleted:
        return abort(501)
    return redirect(f'/posts/{deleted["post_name"]}')
