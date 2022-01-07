# Spotistats

This tool calculates some statistics for Spotify users. Currently supported analyses:

- Intersection of songs of two playlists

## Usage

Clone into this repo:

```
git clone https://github.com/fransie/spotistats.git
```

You need a Spotify App to use this tool. Go to https://developer.spotify.com/dashboard/applications, create an app there
and insert the client id and secret into the credentials file like this:

```
# client id
<YOUR_CLIENT_ID>
# client secret
<YOUR_CLIENT_SECRET>
```

Make sure to never publish your credentials. The .gitignore includes the credentials file.

Replace the username and playlist variables in the main function of ``main.py`` to compare two public playlists.
The program prints the names of the songs that exist in both playlist to stdout.

