from middlewares.user_middlewares import require_login

from flask import Blueprint, render_template, request, make_response, redirect

from mongo import Mongo
import os

# we extract the mongo uri from the env


# we imported the file with mongo that contains the class Mongo
# and we initialize a new connection to mongodb
db = Mongo(os.environ.get("MONGO_URI"))

index = Blueprint('index', __name__)


@index.route("/")
def home():
    # we define a reusable method @ user_authenticate that redirects the
    # page depending on whether the user is logged In or not
    user = require_login(request.cookies)

    if user:
        # true if the user is currently logged in

        if user['role'] == 'student':
            projects = db.fetch_projects()

            return render_template("dashboard/student_dash.html", user_auth=user)

    return render_template("home/index.html")


@index.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # register a new user
        if db.register_user(request.form):
            return "Registered"
        else:
            return render_template("home/register.html", input=request.form, error=True, message=db.fetch_error())
        return "Posted"
    return render_template("home/register.html")


@index.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # authenticate user
        user_fetch = db.login_user(request.form)

        if not user_fetch:

            return render_template("home/login.html", error=True, message=db.fetch_error())

            # no user was found

        response = make_response(redirect("/"))
        response.set_cookie("user_data", user_fetch)
        return response
    return render_template("home/login.html")


@index.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie('user_data')
    return response
