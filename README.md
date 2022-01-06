# Spotistats [WIP]

This tool calculates some statistics for Spotify users. Currently supported analysis:

- Intersection of songs of two playlists

## Usage

Clone into this repo and create a token file:

```
git clone https://github.com/fransie/spotistats.git
cd spotistats
touch token
```

**Authorization is WIP**
First, get a Spotify access token here: https://developer.spotify.com/console/get-several-albums/ by clicking on "Get token"
and login in. Copy the access token into the first line of the file "token". The tokens expire regularly, so
create a new token if you get a corresponding error message.

Replace the username and playlist variables in the main function of ``main.py`` to compare two public playlists.
The program prints the names of the songs that exist in both playlist to stdout.

