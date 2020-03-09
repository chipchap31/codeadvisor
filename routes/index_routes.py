from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os
from middlewares.user_middlewares import require_login
from flask import Blueprint, render_template, request, make_response, redirect, abort
from mongo import database
import json
from math import ceil
index = Blueprint('index', __name__)
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


@index.route("/", methods=["POST", "GET"])
def home():

    # we define a reusable method @ require_login that redirects the
    # page depending on whether the user is logged In or not
    user = require_login(request.cookies)

    # check if the user's cookies exist
    if not user:

        if request.method == 'POST':

            message = Mail(
                from_email='noreply@codeadvisor.ie',
                to_emails=request.form.get('email'),
                subject="noreply",
                html_content=f'''<html>
                                    <body>
                                        
                                        <p>Hello {request.form.get('fullname')},</p>

                                            <p>Thank you for your message! We will get back to you as soon as possible.</p> 

                                            <p>Best regards,</p> 

                                            Code advisor help team 
                                    </body>
                                </html>''')
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
                response = sg.send(message)
                return redirect("/message-ok")
            except Exception as e:
                print(e.message)
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

    top_advisors = database.get_top_advisor()
    # below we render the dashboard
    return render_template('view/dashboard.html', user_auth=user, config={
        "posts": posts_limit,
        "posts_len": posts_len,
        "pagination": ceil(posts_len / 5) + 1,
        'curr_page': curr_page,
        'ref': request.referrer,
        'curr_sort': request.args.get('sort') or 'posted_at',
        'render_next': (curr_page * 5) + len(posts_limit) - 5 < posts_len,
        'top_advisors': top_advisors
    })


@index.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # register a new user
        if database.register_user(request.form):
            return render_template('index/register_ok.html', config={
                'user_name': request.form.get('user_name')
            })
        else:
            return render_template("index/register.html", input=request.form, error=True,
                                   message=database.fetch_error())

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
    """Destroys the cookie defined by logging in"""
    response = make_response(redirect("/"))
    response.delete_cookie('user_data')
    return response


@index.route('/message-ok')
def message():
    return render_template('index/message-ok.html')
