import os

from flask import Flask, request, redirect

from middlewares.user_middlewares import require_login
from routes.index_routes import index
from routes.post_routes import posts

from routes.project_routes import projects
from routes.feedback_routes import feedback
app = Flask(__name__)

app.secret_key = os.environ.get("FLASH_KEY")

app.register_blueprint(index)
app.register_blueprint(projects)
app.register_blueprint(posts)
app.register_blueprint(feedback)


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


@app.before_first_request
def before_first_request_func():
    user = require_login(request.cookies)
    if not user:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
