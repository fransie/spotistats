# Spotistats

This tool calculates some statistics for Spotify users. Currently supported analyses:

- Intersection of songs of two playlists
- Find all playlists of a user that containt a certain song

## Setup

Clone this repo and create a `credentials` file:

```
git clone https://github.com/fransie/spotistats.git
cd spotistats
echo "# client id\n<YOUR_CLIENT_ID>\n# client secret\n<YOUR_CLIENT_SECRET>" > credentials
```

You need a Spotify App to use this tool. Go to https://developer.spotify.com/dashboard/applications and create an app there.
Insert the obtained client id and secret of your app into the `credentials` file:

```
# client id
<YOUR_CLIENT_ID>
# client secret
<YOUR_CLIENT_SECRET>
```

:warning: Make sure never to publish your credentials!

Next, in your Spotify App, click "Edit Settings", add the following string to "Redirect URIs":
`http://localhost:8080` and save the settings.

## Usage

Go to the folder `spotitats`, run the command `flask run` and go to http://127.0.0.1:5000/ to use the app.
The analyses are pretty slow right now, so please wait until the browser finishes loading.