import spotipy
from markupsafe import escape
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request

import stats

app = Flask(__name__)


def authorize():
    cred_file = open('credentials', 'r')
    lines = cred_file.readlines()
    [cid, secret] = [lines[1].strip("\n"), lines[3].strip("\n")]
    scope = "playlist-read-private playlist-read-collaborative"
    redirect = "http://localhost:8080"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret,
                                                     redirect_uri=redirect, scope=scope))


stats = stats.Stats(authorize())


@app.route("/")
def index():
    return render_template('UI.html')


@app.route("/common-songs", methods=['POST'])
def get_common_songs():
    u1 = escape(request.form["u1name"])
    u2 = escape(request.form["u2name"])
    p1 = escape(request.form["u1playlist"])
    p2 = escape(request.form["u2playlist"])
    songs = stats.find_common_songs(u1, p1, u2, p2)
    return render_template("songs.html", songs=songs)


@app.route("/song_in_playlists", methods=['POST'])
def find_song_in_playlists():
    username = escape(request.form["uname"])
    link = str(escape(request.form["link"]))
    song_id = link[len("https://open.spotify.com/track/"):]
    playlists = stats.find_song_in_playlists(username, song_id)
    return render_template("song_in_playlists.html", playlists=playlists)


if __name__ == "__main__":
    app.run()
