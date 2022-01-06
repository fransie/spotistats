import requests
import json

TOKEN = ""


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
            # TODO: add automatic token support
            print(response.text)
            exit(-1)
        playlists_json = json.loads(response.text)
        for item in playlists_json["items"]:
            if item["name"] == self.name:
                self.id = item["id"]
                self.length = item["tracks"]["total"]
        self.request_songs()

    def request_songs(self):
        for i in range(0, self.length+1, 100):
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{self.id}/tracks?limit=100&offset={i}",
                headers={"Authorization": f"Bearer {TOKEN}"})
            songs_json = json.loads(response.text)
            for item in songs_json["items"]:
                # TODO: add multiple artists
                song = Song(item["track"]["name"], item["track"]["artists"][0]["name"])
                self.songs.append(song)


if __name__ == '__main__':
    token_file = open('token', 'r')
    TOKEN = token_file.readline()

    user1 = "USERNAME1"
    playlist1_name = "PLAYLIST1"
    playlist1 = Playlist(playlist1_name, user1)
    playlist1.initialise_data()

    user2 = "USERNAME2"
    playlist2_name = "PLAYLIST2"
    playlist2 = Playlist(playlist2_name, user2)
    playlist2.initialise_data()

    for song1 in playlist1.songs:
        for song2 in playlist2.songs:
            if song2.name == song1.name and song2.artist == song1.artist:
                print(song1.name)
