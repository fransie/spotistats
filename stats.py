from spotipy import Spotify


class Song:
    """A Spotify song"""

    def __init__(self, song_json):
        self.name = song_json["track"]["name"]
        self.id = song_json["track"]["id"]
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
    """A Spotify user with their playlists"""

    def __init__(self, username, client: Spotify):
        self.userid = client.user(username)["id"]
        self.playlists = self.get_playlists(client)

    def get_playlists(self, client: Spotify):
        playlists = []
        response = client.user_playlists(user=self.userid, limit=50)
        num_of_playlists = response["total"]
        for playlist in response["items"]:
            playlists.append(Playlist(playlist))
        for i in range(50, num_of_playlists + 1, 50):
            response = client.user_playlists(user=self.userid, limit=50, offset=i)
            for playlist in response["items"]:
                playlists.append(Playlist(playlist))
        return playlists

    def get_playlist_by_name(self, name):
        playlist_list = [playlist for playlist in self.playlists if playlist.name == name]
        if len(playlist_list) == 0:
            # TODO: error handling here
            print(f"No playlist with name {name} by user {self.userid} found.")
            exit()
        else:
            playlist = playlist_list[0]
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

    def init_songs(self, client: Spotify):
        for i in range(0, self.length + 1, 100):
            response = client.playlist_items(playlist_id=self.id)
            # filter out null songs sent by Spotify API
            songs = [x for x in response["items"] if x["track"] is not None]
            for song_json in songs:
                song = Song(song_json)
                self.songs.append(song)


class Stats:
    # TODO: caching of users, playlists, songs
    def __init__(self, spoti_client: Spotify):
        self.client = spoti_client

    def find_common_songs(self, u1, p1, u2, p2):
        user1 = User(u1, self.client)
        user2 = User(u2, self.client)

        playlist1 = user1.get_playlist_by_name(p1)
        playlist2 = user2.get_playlist_by_name(p2)
        playlist1.init_songs(self.client)
        playlist2.init_songs(self.client)

        common_songs = []
        for song1 in playlist1.songs:
            for song2 in playlist2.songs:
                if song1 == song2:
                    common_songs.append(song1)
        return common_songs

    def find_song_in_playlists(self, user, song_id):
        user = User(user, self.client)
        hit_playlists = []
        for playlist in user.playlists:
            playlist.init_songs(self.client)
            for song in playlist.songs:
                if song.id == song_id:
                    hit_playlists.append(playlist)
                    break
        return hit_playlists
