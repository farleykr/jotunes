from flask import Blueprint, current_app, render_template
from jo_tunes.main.api_handler import random_songs

main = Blueprint('app', __name__)

@main.route("/")
def home():
    playlist = random_songs()
    return render_template('home.html', playlist=playlist)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

