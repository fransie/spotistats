from pprint import pprint

import requests
import json

from markupsafe import escape
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request

from stats import find_common_songs

app = Flask(__name__)
TOKEN = ""


@app.route("/")
def index():
    return render_template('UI.html')


@app.route("/common-songs", methods=['POST'])
def get_common_songs():
    u1 = escape(request.form["u1name"])
    u2 = escape(request.form["u2name"])
    p1 = escape(request.form["u1playlist"])
    p2 = escape(request.form["u2playlist"])
    songs = find_common_songs(u1, p1, u2, p2)
    return render_template("songs.html", songs=songs)


@app.before_first_request
def authorize():
    cred_file = open('credentials', 'r')
    lines = cred_file.readlines()
    credentials = [lines[1].strip("\n"), lines[3].strip("\n")]

    client_credentials_manager = SpotifyClientCredentials(credentials[0], credentials[1])
    global TOKEN
    TOKEN = client_credentials_manager.get_access_token(False)
