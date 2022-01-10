import json
import requests

TOKEN = ""


class Song:
    """A Spotify song"""

    def __init__(self, song_json):
        self.name = song_json["track"]["name"]
        self.artists = []
        self.get_artists(song_json)

    def __str__(self):
        string = f'"{self.name}" by {self.artists[0]}'
        for artist in self.artists[1:]:
            string += f", {artist}"
        return string

    def __eq__(self, other):
        if isinstance(other, Song):
            return self.name == other.name and self.artists == other.artists
        return False

    def get_artists(self, song_json):
        for artist in song_json["track"]["artists"]:
            artist_name = artist["name"]
            self.artists.append(artist_name)


class User:
    """A Spotify user"""

    def __init__(self, userid):
        self.userid = userid
        self.playlists = self.get_playlists()

    def get_playlists(self):
        playlists = []
        response = requests.get(f"https://api.spotify.com/v1/users/{self.userid}/playlists?limit=50",
                                headers={"Authorization": f"Bearer {TOKEN}"})
        playlists_json = parse_response(response, "get playlists of user")
        num_of_playlists = playlists_json["total"]
        for playlist in playlists_json["items"]:
            playlists.append(Playlist(playlist))
        for i in range(50, num_of_playlists + 1, 50):
            response = requests.get(f"https://api.spotify.com/v1/users/{self.userid}/playlists?limit={50}&offset={i}",
                                    headers={"Authorization": f"Bearer {TOKEN}"})
            playlists_json = parse_response(response, "get playlists")
            for playlist in playlists_json["items"]:
                playlists.append(Playlist(playlist))
        return playlists

    def get_playlist_by_name(self, name):
        playlist_list = [playlist for playlist in self.playlists if playlist.name == name]
        if len(playlist_list) == 0:
            print(f"No playlist with name {name} by user {self.userid} found.")
            exit()
        else:
            playlist = playlist_list[0]
            playlist.init_songs()
            return playlist


class Playlist:
    """A Spotify playlist"""

    def __init__(self, json_string):
        self.id = json_string["id"]
        self.name = json_string["name"]
        self.json = json_string
        self.owner = json_string["owner"]["id"]
        self.length = json_string["tracks"]["total"]
        self.songs = []

    def init_songs(self):
        for i in range(0, self.length + 1, 100):
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{self.id}/tracks?limit=100&offset={i}",
                headers={"Authorization": f"Bearer {TOKEN}"})
            songs_json = parse_response(response, "get playlist")["items"]
            # filter out null songs sent by Spotify API
            songs = [x for x in songs_json if x["track"] is not None]
            for song_json in songs:
                song = Song(song_json)
                self.songs.append(song)


def parse_response(response, action: str):
    if response.status_code != 200:
        print(f"Request for action '{action}' failed: {response.text}")
        exit(-1)
    else:
        return json.loads(response.text)


def find_common_songs(u1, p1, u2, p2):
    user1 = User(u1)
    user2 = User(u2)
    playlist1 = user1.get_playlist_by_name(p1)
    playlist2 = user2.get_playlist_by_name(p2)
    common_songs = []
    for song1 in playlist1.songs:
        for song2 in playlist2.songs:
            if song1 == song2:
                common_songs.append(song1)
    return common_songs
