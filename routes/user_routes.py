import json
from datetime import datetime


from flask import Blueprint, render_template, request, redirect, make_response
from middlewares.user_middlewares import require_student, require_login
from mongo import database


users = Blueprint('users', __name__)


@users.route("/<username>")
def profile(username):
    user = require_login(request.cookies)
    data = database.fetch_user(username)
    if not data:
        return {}

    return render_template("users/profile.html", user_auth=user, curr_user=data)
