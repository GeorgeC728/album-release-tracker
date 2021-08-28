# Load required libraries
import json                 # For working with JSON data

# Load the api key
with open("api-key.json") as file:
    API_KEY = json.load(file)["api_key"]

