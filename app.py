from mongo import Mongo
from flask import Flask, render_template, request, make_response, redirect
import os

app = Flask(__name__)


MONGO_URI = os.environ.get("MONGO_URI")

db = Mongo(MONGO_URI)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():

    return "Hello register!"


if __name__ == "__main__":

    app.run(debug=True)
