# Spotistats

This tool calculates some statistics for Spotify users. Currently supported analyses:

- Intersection of songs of two playlists

## Usage

Clone into this repo and create a credentials file:

```
git clone https://github.com/fransie/spotistats.git
cd spotistats
echo "# client id\n<YOUR_CLIENT_ID>\n# client secret\n<YOUR_CLIENT_SECRET>" > credentials
```

You need a Spotify App to use this tool. Go to https://developer.spotify.com/dashboard/applications, create an app there
and insert the obtained client id and secret of your app into the credentials file:

```
# client id
<YOUR_CLIENT_ID>
# client secret
<YOUR_CLIENT_SECRET>
```

Make sure to never publish your credentials. The .gitignore includes the credentials file.

Replace the username and playlist variables in the main function of ``main.py`` to compare two public playlists.
The program prints the names of the songs that exist in both playlist to stdout.

