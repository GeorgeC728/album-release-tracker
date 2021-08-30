#### Perform required set up

# Load required libraries
import json                                                 # For working with JSON data
import spotipy                                              # Python wrapper for spotify API
from spotipy.oauth2 import SpotifyClientCredentials         # Allows access non-user data for spotify API
from spotipy.oauth2 import SpotifyOAuth                     # Allows acessing user data for spotify API
import os                                                   # Used for setting environment variables
import pandas as pd                                         # For wrangling data
from datetime import date, datetime, timedelta

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
spotify_client = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope))

# These variables are used to loop through the users library until the end is reached
tracks_count = 50
i = 0

# Create an empty datafram to save the artist URIs in
artist_uri_df = pd.DataFrame(columns = ["artist"])

# Only 50 of the users tracks can be obtained at one time but the offset argument can allow the next 50 to be read.
# If 50 tracks are requested but less than 50 comeback then the entire library has been read
while tracks_count == 50:
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

# The dataframe produced above will have duplicated artists so make a unique list
artist_uri_unique = artist_uri_df["artist"].unique()

print(len(artist_uri_unique))

# We no longer need access to the users library so use the appropriate client
spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Calculate the date cut off - 7 days from before. This could be modified to be more variable
date_cutoff = date.today() - timedelta(days = 7)

recent_album_df = pd.DataFrame(columns = ["name", "artist", "release_date"])

# Loop through the artists just found
for artist_uri in artist_uri_unique:
    # Get list of albums 
    album_list = spotify_client.artist_albums(artist_uri, album_type = "album")["items"]

    # Check if artist has any albums
    if len(album_list) != 0:
        # Get latest album
        latest_album = album_list[0]
        # Need to extract a release date. How this is done depends on the release date precision
        if latest_album["release_date_precision"] == "day" :
            # If we've got precision to a single day, extract in ISO format (yyyy-mm-dd)
            album_release_date = date.fromisoformat(latest_album["release_date"])
        if latest_album["release_date_precision"] == "month":
            # If its to months, extract in the form yyyy-mm
            album_release_date = datetime.strptime(latest_album["release_date"], "%Y-%m").date()
        if latest_album["release_date_precision"] == "year":
            # If only to year, extract in the form yyyy
            album_release_date = datetime.strptime(latest_album["release_date"], "%Y").date()

        # Check if the album was released since the predefined date cut off
        if album_release_date >= date_cutoff:
            # Get the album name
            album_name = latest_album["name"]
            # Get the artist
            album_artist = latest_album["artists"][0]["name"]
            # Create a row to append in the form of a data frame
            album_to_append_df = pd.DataFrame(
                [[album_name, album_artist, album_release_date]],
                columns = ["name", "artist", "release_date"])
            # Append the row to the maste dataframe
            recent_album_df = recent_album_df.append(album_to_append_df)
            # Save album

print(recent_album_df)

# Save data
recent_album_df.to_csv("data.csv")


