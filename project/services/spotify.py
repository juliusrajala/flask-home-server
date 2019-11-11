import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = str(os.environ.get("SPOTIFY_CLIENT_ID", ''))
client_secret = str(os.environ.get("SPOTIFY_CLIENT_SECRET", ''))

def init_search_service():
    if client_id == '' or client_secret == '':
        raise Exception('Invalid spotify authorization')
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(client_credentials_manager=credentials_manager)
    return spotipy_client

def register_player_account():
    """ Using the spotify authorization code flow. """
    # Request authorization to access data
    # client_id, response_type, redirect_uri, state, scope

    # Prompt user to log in
    # Log in using desired credentials here on server-side.

    # Request access and refresh tokens
    # Store access token for usage with API calls
    # If token is about to expire, request new token

class PlayerService(object):
    def __init__(self):
        self.client_id = client_id
        self.access_token = ''

    def request_access_token(self):
        print("Do thing")

    def refresh_access_token(self):
        print("Do thing")


    # Client controls
    def play_next(self):
        print("Play next")

    def play_last(self):
        print("Play last")

    def add_to_queue(self):
        print("Add to queue")

    def get_playing_now(self):
        print("Get now playing song")

    def get_queue(self):
        print("Get account queue")
