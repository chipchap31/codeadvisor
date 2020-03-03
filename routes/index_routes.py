from middlewares.user_middlewares import require_login
from flask import Blueprint, render_template, request, make_response, redirect, abort
from mongo import database
import json

index = Blueprint('index', __name__)


@index.route("/")
def home():
    print(list(database.getTopAdvisor()))

    # we define a reusable method @ require_login that redirects the
    # page depending on whether the user is logged In or not
    user = require_login(request.cookies)

    # check if the user's cookies exist
    if not user:
        return render_template('index/index.html')

    # fetch all of the posts of the students
    posts = database.post_fetch(sort=request.args.get(
        'sort') or 'posted_at')  # returns the posts of all students
    posts_len = len(posts)

    curr_page = int(request.args.get('page')
                    ) if request.args.get('page') else 1

    if curr_page == 1:
        posts_limit = posts[:5]
    else:

        posts_limit = posts[(5 * curr_page) - 5: ((5 * curr_page) - 5) * 2]

    # below we render the dashboard
    return render_template('view/dashboard.html', user_auth=user, config={
        "posts": posts_limit,
        "posts_len": posts_len,
        "pagination": round(posts_len / 5) + 2,
        'curr_page': curr_page,
        'ref': request.referrer,
        'curr_sort': request.args.get('sort') or 'posted_at',
        'render_next': (curr_page * 5) + len(posts_limit) - 5 < posts_len,
    })


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
            # no user  found
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
