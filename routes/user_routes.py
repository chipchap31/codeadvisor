import json
from datetime import datetime


from flask import Blueprint, render_template, request, redirect, make_response,abort
from middlewares.user_middlewares import require_login
from mongo import database


users = Blueprint('users', __name__)


@users.route("/<username>")
def profile(username):
    """Renders the profile info of the user"""
    user = require_login(request.cookies)
    data = database.fetch_user(username)
    if not data:
        return {}
    top_advisors = database.get_top_advisor()
    return render_template("users/profile.html", config={
        "top_advisors": top_advisors
    }, referrer=request.referrer, user_auth=user, curr_user=data)


@users.route("/<username>/edit", methods=["GET", "POST"])
def profiel_edit(username):
    """Renders the profile info of the user"""
    user = require_login(request.cookies)
    
    if request.method == 'POST':
        if database.edit_user({**request.form,'_id' :user['_id']}):
            return redirect(f"/{ user['user_name'] }")

    top_advisors = database.get_top_advisor()
    data = database.fetch_user(username)
    return render_template("users/profile_edit.html", user_auth=user, config={
        "referrer": request.referrer,
        'top_advisors': top_advisors,
        "profile": data
    })


@users.route("/<user_name>/delete", methods=["POST"])
def user_delete(user_name):
    user = require_login(request.cookies)
    if not database.delete_account({'_id': user['_id'],
        'user_name': user_name}):
        return abort(500)
    response = make_response(redirect("/"))
    response.delete_cookie('user_data')
    return response
    