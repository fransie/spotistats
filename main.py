import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials


class Song:
    """A Spotify song"""

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


class Playlist:
    """A Spotify playlist"""

    def __init__(self, name, userid):
        self.name = name
        self.id = None
        self.owner = userid
        self.length = None
        self.songs = []

    def initialise_data(self):
        response = requests.get(f"https://api.spotify.com/v1/users/{self.owner}/playlists",
                                headers={"Authorization": f"Bearer {TOKEN}"})
        if response.status_code != 200:
            print(response.text)
            exit(-1)
        playlists_json = json.loads(response.text)
        for item in playlists_json["items"]:
            if item["name"] == self.name:
                self.id = item["id"]
                self.length = item["tracks"]["total"]
        self.request_songs()

    def request_songs(self):
        for i in range(0, self.length + 1, 100):
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{self.id}/tracks?limit=100&offset={i}",
                headers={"Authorization": f"Bearer {TOKEN}"})
            songs_json = json.loads(response.text)
            for item in songs_json["items"]:
                # TODO: add multiple artists
                song = Song(item["track"]["name"], item["track"]["artists"][0]["name"])
                self.songs.append(song)


def authorize():
    cred_file = open('credentials', 'r')
    lines = cred_file.readlines()
    credentials = [lines[1].strip("\n"), lines[3].strip("\n")]

    client_credentials_manager = SpotifyClientCredentials(credentials[0], credentials[1])
    return client_credentials_manager.get_access_token(False)


def find_common_songs(p1, p2):
    common_songs = []
    for song1 in p1.songs:
        for song2 in p2.songs:
            if song2.name == song1.name and song2.artist == song1.artist:
                common_songs.append(song1)
    return common_songs


if __name__ == '__main__':
    TOKEN = authorize()

    user1 = "USERNAME1"
    playlist1_name = "PLAYLIST1"
    playlist1 = Playlist(playlist1_name, user1)
    playlist1.initialise_data()

    user2 = "USERNAME2"
    playlist2_name = "PLAYLIST2"
    playlist2 = Playlist(playlist2_name, user2)
    playlist2.initialise_data()

    songs = find_common_songs(playlist1, playlist2)
    for s in songs:
        print(s.name)
