from mongo import Mongo
from flask import Flask, render_template, request, make_response, redirect
import os

app = Flask(__name__)

# we extract the mongo uri from the env
MONGO_URI = os.environ.get("MONGO_URI")

# we imported the file with mongo that contains the class Mongo
# and we initialize a new connection to mongodb
db = Mongo(MONGO_URI)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():

    return render_template("register.html")


if __name__ == "__main__":

    app.run(debug=True)
