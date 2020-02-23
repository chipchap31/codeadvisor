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

    print(request.cookies)
    return request.cookies
