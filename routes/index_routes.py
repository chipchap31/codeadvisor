from middlewares.user_middlewares import require_login

from flask import Blueprint, render_template, request, make_response, redirect
import requests
from mongo import database
import json

index = Blueprint('index', __name__)


@index.route("/")
def home():
    # we define a reusable method @ user_authenticate that redirects the
    # page depending on whether the user is logged In or not
    user = require_login(request.cookies)

    if user:
        # true if the user is currently logged in

        if user['role']:
            return render_template("view/dashboard.html", sort=request.args.get('sort') or 'Newest', user_auth=user,
                                   projects=database.fetch_projects({
                                       "user": None,
                                       "sort": request.args.get('sort'),
                                       "limit": request.args.get("limit")
                                   }))

        return render_template("view/set_role.html", user_auth=user)
    return render_template("index/index.html")


@index.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # register a new user
        if database.register_user(request.form):
            return "Registered"
        else:
            return render_template("index/register.html", input=request.form, error=True,
                                   message=database.fetch_error())
        return "Posted"
    return render_template("index/register.html")


@index.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # authenticate user
        user_fetch = database.login_user(request.form)

        if not user_fetch:
            # no user was found
            return render_template("index/login.html", error=True, message=database.fetch_error())

        response = make_response(redirect("/"))
        response.set_cookie("user_data", user_fetch)
        return response
    return render_template("index/login.html")


@index.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie('user_data')
    return response


@index.route("/select_role")
def select_role():
    user = require_login(request.cookies)
    if user:
        role = request.args.get("role")
        database.set_role(user['user_name'], role)
        response = make_response(redirect("/"))
        user['role'] = role

        response.set_cookie("user_data", json.dumps(user))
        return response
