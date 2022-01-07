from pprint import pprint

import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials


class Song:
    """A Spotify song"""

    def __init__(self, name, artists: list):
        self.name = name
        self.artists = artists

    def __str__(self):
        string = f'"{self.name}" by {self.artists[0]}'
        for artist in self.artists[1:]:
            string += f", {artist}"
        return string


class User:
    """A Spotify user"""

    def __init__(self, userid):
        self.userid = userid
        self.number_of_playlists = self.get_playlists()

    def get_playlists(self):
        response = requests.get(f"https://api.spotify.com/v1/users/{self.userid}/playlists?limit=1",
                                headers={"Authorization": f"Bearer {TOKEN}"})
        if response.status_code != 200:
            print(f"Request to get playlists of user {self.userid} failed: {response.text}")
            exit(-1)
        else:
            return json.loads(response.text)["total"]


class Playlist:
    """A Spotify playlist"""

    def __init__(self, name, user: User):
        self.name = name
        self.id = None
        self.owner = user
        self.length = None
        self.songs = []

    def initialise_data(self):
        for i in range(0, self.owner.number_of_playlists + 1, 50):
            response = requests.get(
                f"https://api.spotify.com/v1/users/{self.owner.userid}/playlists?limit=50&offset={i}",
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
                    return
        if self.id == None:
            print(f"No playlist with the name {self.name} found.")
            exit()

    def request_songs(self):
        for i in range(0, self.length + 1, 100):
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{self.id}/tracks?limit=100&offset={i}",
                headers={"Authorization": f"Bearer {TOKEN}"})
            songs_json = json.loads(response.text)["items"]
            # filter out null songs sent by Spotify API
            songs = [x for x in songs_json if x["track"] is not None]
            for song in songs:
                song_name = song["track"]["name"]
                song_artists = []
                for artist in song["track"]["artists"]:
                    artist_name = artist["name"]
                    song_artists.append(artist_name)
                self.songs.append(Song(song_name, song_artists))


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
            if song2.name == song1.name and song2.artists == song1.artists:
                common_songs.append(song1)
    return common_songs


if __name__ == '__main__':
    TOKEN = authorize()

    user1 = User("USERNAME1")
    playlist1_name = "PLAYLIST1"
    playlist1 = Playlist(playlist1_name, user1)
    playlist1.initialise_data()

    user2 = User("USERNAME2")
    playlist2_name = "PLAYLIST2"
    playlist2 = Playlist(playlist2_name, user2)
    playlist2.initialise_data()

    songs = find_common_songs(playlist1, playlist2)
    for s in songs:
        print(s)
