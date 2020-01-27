from mongo import Mongo
from flask import Blueprint, Flask, render_template, request, make_response, redirect
import os
from middlewares.user_middlewares import require_login

from routes.user_routes import user
app = Flask(__name__)

app.register_blueprint(user)
# we extract the mongo uri from the env
MONGO_URI = os.environ.get("MONGO_URI")

# we imported the file with mongo that contains the class Mongo
# and we initialize a new connection to mongodb
db = Mongo(MONGO_URI)


@app.route("/")
def index():
    # we define a reusable method @ user_authenticate that redirects the
    # page depending on whether the user is logged In or not
    user = require_login(request.cookies)
    print(user)
    if user:
        # true if the user is currently logged in
        return redirect("/" + user["user_name"])
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # register a new user
        if db.register_user(request.form):
            return "Registered"
        else:
            return render_template("register.html", input=request.form, error=True, message=db.fetch_error())
        return "Posted"
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # authenticate user
        user_fetch = db.login_user(request.form)

        if not user_fetch:

            return render_template("login.html", error=True, message=db.fetch_error())

            # no user was found

        response = make_response(redirect("/"))
        response.set_cookie("user_data", user_fetch)
        return response
    return render_template("login.html")


@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie('user_data')
    return response


if __name__ == "__main__":

    app.run(debug=True)
