import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token

client_id = str(os.environ.get('SPOTIFY_CLIENT_ID', ''))
client_secret = str(os.environ.get('SPOTIFY_CLIENT_SECRET', ''))
spotify_username = str(os.environ.get('SPOTIFY_USERNAME', ''))
spotify_redirect = str(os.environ.get('SPOTIFY_REDIRECT_URL', ''))

def init_search_service():
    if client_id == '' or client_secret == '':
        raise Exception('Invalid client_id or client_secret')
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(client_credentials_manager=credentials_manager)
    return spotipy_client

class PlayerService:
    """Using the spotify authorization code flow. """
    def __init__(self, client):
        self.access_token = ''
        print(f'Initializing client with {client}')
        self.client = client
        self.is_player_client = False

        if client_id == '' or client_secret == '' or spotify_redirect == '':
            raise Exception('Invalid spotify authorization')

        client_scope = "user-modify-playback-state user-read-currently-playing user-read-playback-state"
        try:
            prompt_for_user_token(
                username=spotify_username,
                scope=client_scope,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=spotify_redirect
            )
        except (EOFError):
            print('Error while reading input')

    def inject_token(self, auth_code):
        self.access_token = auth_code
        if auth_code == '':
            raise Exception('Bad auth_code')

        self.client = spotipy.Spotify(auth=auth_code)
        self.is_player_client = True
        return self.client
