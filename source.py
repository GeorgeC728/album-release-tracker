# Load required libraries
import json                                                 # For working with JSON data
import spotipy                                              # Python wrapper for spotify API
from spotipy.oauth2 import SpotifyClientCredentials         # Credential manager for spotify API
import os                                                   # Used for setting environment variables


# Load the api key

api_json = json.load(open("api-key.json"))

os.environ["SPOTIPY_CLIENT_ID"] = api_json["client_id"]
os.environ["SPOTIPY_CLIENT_SECRET"] = api_json["client_secret"]
os.environ["SPOTIPY_REDIRECT_URI"] = api_json["redirect_uri"]


tool_uri = 'spotify:artist:2yEwvVSSSUkcLeSTNyHKh8'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(tool_uri, album_type='album')

albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])