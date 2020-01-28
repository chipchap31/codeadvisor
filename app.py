
from flask import Flask


from routes.index_routes import index


app = Flask(__name__)


app.register_blueprint(index)


if __name__ == "__main__":

    app.run(debug=True)
