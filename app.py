import os

from flask import Flask

from routes.index_routes import index
from routes.user_routes import users
from routes.project_routes import projects
app = Flask(__name__)

app.secret_key = os.environ.get("FLASH_KEY")

app.register_blueprint(index)
app.register_blueprint(users)
app.register_blueprint(projects)
if __name__ == "__main__":
    app.run(debug=True)
