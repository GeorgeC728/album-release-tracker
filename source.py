#### Perform required set up

# Load required libraries
import json                                                 # For working with JSON data
import spotipy                                              # Python wrapper for spotify API
from spotipy.oauth2 import SpotifyClientCredentials         # Allows access non-user data for spotify API
from spotipy.oauth2 import SpotifyOAuth                     # Allows acessing user data for spotify API
import os                                                   # Used for setting environment variables
import pandas as pd                                         # For wrangling data

# Load the api key
api_json = json.load(open("api-key.json"))

# Set environment variables as required by spotipy
os.environ["SPOTIPY_CLIENT_ID"] = api_json["client_id"]
os.environ["SPOTIPY_CLIENT_SECRET"] = api_json["client_secret"]
os.environ["SPOTIPY_REDIRECT_URI"] = api_json["redirect_uri"]

#### Get list of a users liked artists

# This scope is needed to read libraries
scope = "user-library-read"

# Authenticate with the spotify API
spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# These variables are used to loop through the users library until the end is reached
tracks_count = 500
i = 0

# Create an empty datafram to save the artist URIs in
artist_uri_df = pd.DataFrame(columns = ["artist"])

# Only 50 of the users tracks can be obtained at one time but the offset argument can allow the next 50 to be read.
# If 50 tracks are requested but less than 50 comeback then the entire library has been read
while tracks_count != 50:
    # Request 50 tracks
    tracks = spotify_client.current_user_saved_tracks(limit = 50, offset = i * 50)["items"]
    # See how many tracks were returned - this will break the loop if needed
    tracks_count = len(tracks)

    # Loop through the tracks received
    for track in tracks:
        # For each track, get the artists - there may be more than one, x ft. y for example
        # Getting additional artists may not be desired 
        artist_multiple = track["track"]["artists"]
        # Loop through the artists for a given track
        for artist in artist_multiple:
            # Get the uri
            artist_single_uri = artist["uri"]
            # Convert the uri to a data frame
            artist_single_uri_df = pd.DataFrame([artist_single_uri], columns = ["artist"])
            # Append the single artist to the full list
            artist_uri_df = artist_uri_df.append(artist_single_uri_df)
    # Increment i, this ensures the next 50 tracks are read in
    i += 1

print(artist_uri_df["artist"].unique())


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

#results = sp.current_user_saved_tracks(limit = 50, offset = 0)
#for idx, item in enumerate(results['items']):
#    track = item['track']
#    print(idx, track['artists'][0]['name'], " – ", track['name'])