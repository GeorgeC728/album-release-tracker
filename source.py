# Load required libraries
import json                                                 # For working with JSON data
import spotipy                                              # Python wrapper for spotify API
#from spotipy.oauth2 import SpotifyClientCredentials         # Credential manager for spotify API
from spotipy.oauth2 import SpotifyOAuth
import os                                                   # Used for setting environment variables
import pandas as pd                                         # pandas for wrangling data

# Load the api key

api_json = json.load(open("api-key.json"))

os.environ["SPOTIPY_CLIENT_ID"] = api_json["client_id"]
os.environ["SPOTIPY_CLIENT_SECRET"] = api_json["client_secret"]
os.environ["SPOTIPY_REDIRECT_URI"] = api_json["redirect_uri"]


#tool_uri = 'spotify:artist:2yEwvVSSSUkcLeSTNyHKh8'
#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#
#results = spotify.artist_albums(tool_uri, album_type='album')
#
#albums = results['items']
#while results['next']:
#    results = spotify.next(results)
#    albums.extend(results['items'])
#
#for album in albums:
#    print(album["name"])
#    print(album["release_date"])


scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

tracks_count = 500
i = 0

artist_uri_df = pd.DataFrame(columns = ["artist"])

while tracks_count != 50:
    tracks = sp.current_user_saved_tracks(limit = 50, offset = i * 50)["items"]
    tracks_count = len(tracks)
    for j in range(0, tracks_count - 1):
        artist_multiple_uri = tracks[j]["track"]["artists"]
        for k in range(0, len(artist_multiple_uri)):
            artist_single_uri = [tracks[j]["track"]["artists"][k]["uri"]]
            artist_single_uri_df = pd.DataFrame(artist_single_uri, columns = ["artist"])
            artist_uri_df = artist_uri_df.append(artist_single_uri_df)
    i += 1

print(artist_uri_df["artist"].unique())

#results = sp.current_user_saved_tracks(limit = 50, offset = 0)
#for idx, item in enumerate(results['items']):
#    track = item['track']
#    print(idx, track['artists'][0]['name'], " – ", track['name'])