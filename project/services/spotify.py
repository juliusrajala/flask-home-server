import os
import spotipy
import spotipy.oauth2 as SPOauth
import webbrowser
from spotipy.util import prompt_for_user_token
from enum import Enum

client_id = str(os.environ.get('SPOTIFY_CLIENT_ID', ''))
client_secret = str(os.environ.get('SPOTIFY_CLIENT_SECRET', ''))
spotify_username = str(os.environ.get('SPOTIFY_USERNAME', ''))
redirect_uri = str(os.environ.get('SPOTIFY_REDIRECT_URL', ''))

def build_auth_uri(secret):
    client_scope = "user-modify-playback-state user-read-currently-playing user-read-playback-state"
    return ''.join([
        'https://accounts.spotify.com/authorize?client_id=',
        client_id,
        '&response_type=code&redirect_uri=',
        redirect_uri,
        '&scope=',
        client_scope,
        '&state=',
        secret
    ])

def init_search_service():
    if client_id == '' or client_secret == '':
        raise Exception('Invalid client_id or client_secret')
    credentials_manager = SPOauth.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(client_credentials_manager=credentials_manager)
    return spotipy_client

class PlayerService:
    """Using the spotify authorization code flow. """
    def __init__(self, client):
        self.registration_secret = ''
        self.is_player_client = False

        self.access_token = ''
        self.client = client

    def set_registered(self, secret):
        self.registration_secret = secret

    def inject_token(self, auth_code):
        self.access_token = auth_code
        if auth_code == '':
            raise Exception('Bad auth_code')

        self.client = spotipy.Spotify(auth=auth_code)
        self.is_player_client = True
        return self.client
