# Album release tracker
# About
This is a script that connects to your Spotify library and creates a list of new releases (last 7 days) by the artists you like. It makes use of the Spotify API availible [here](https://developer.spotify.com/documentation/web-api/).

# Usage

## Obtaining API credentials
The script requires API credentials for the Spotify API. These can be obtained through the API dashboard [here](https://developer.spotify.com/dashboard/).
- Login/create an account
- Select create an app
- Give your app a name/description
- Once your app has been created, go to settings and under redirect URI, add something for it to redirect to. This doesn't really matter but I use https://localhost
- On the overview page, you can view your client id/secrets. These need to be stored for the python script to use.
- Create a file in the repo folder called `api-key.json` in the format:
```{json}
{
    "client_id":"CLIENT ID GOES HERE",
    "client_secret":"CLIENT SECRET GOES HERE",
    "redirect_uri":"REDIRECT URI GOES HERE"
}
```

## Running the script

The first time running the script will require some interaction. Hit run and it will redirect you to your redirect URI, asking you to login and give access. Once this is done you may need to copy the URL and give it back to the script. Keep and eye on the terminal, it will tell you what to do there. Access tokens are then saved to the `.cache` file. This can be saved and moved around to run the script without interaction, although be careful as you could give someone else control of your Spotify account/data. 

## Outputs

The script outputs the releases into the file `data.csv`.

# Roadmap

Features that will come in the future:
- Functionality to email the results to the user
- Containerise so this can scheduled easily.
