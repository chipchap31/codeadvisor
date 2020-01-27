# facebook/views/user.py

from flask import Blueprint, render_template

user = Blueprint('user', __name__)


@user.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('index.html')


@user.route('/<user_url_slug>/photos')
def photos(user_url_slug):
    # Do some stuff
    return render_template('user/photos.html')


@user.route('/<user_url_slug>/about')
def about(user_url_slug):
    # Do some stuff
    return render_template('user/about.html')
