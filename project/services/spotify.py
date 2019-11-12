import os
import spotipy
import spotipy.oauth2 as spoAuth2
import json
import requests

client_id = str(os.environ.get('SPOTIFY_CLIENT_ID', ''))
client_secret = str(os.environ.get('SPOTIFY_CLIENT_SECRET', ''))
spotify_username = str(os.environ.get('SPOTIFY_USERNAME', ''))
redirect_uri = str(os.environ.get('SPOTIFY_REDIRECT_URL', ''))
token_endpoint = 'https://accounts.spotify.com/api/token'


def build_auth_uri(secret):
    client_scope = "user-modify-playback-state user-read-currently-playing user-read-playback-state user-read-private"
    return ''.join([
        'https://accounts.spotify.com/authorize?client_id=',
        client_id,
        '&response_type=code&redirect_uri=',
        redirect_uri,
        '&scope=',
        client_scope,
        '&state=',
        secret,
        '&show_dialog=true'
    ])


def init_search_service():
    if client_id == '' or client_secret == '':
        raise Exception('Invalid client_id or client_secret')
    credentials_manager = spoAuth2.SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(
        client_credentials_manager=credentials_manager)
    return spotipy_client


class PlayerService:
    """Using the spotify authorization code flow. """

    def __init__(self, client):
        self.registration_secret = ''
        self.is_player_client = False

        self.access_token = ''
        self.client = client

    def _post(self, data):
        return requests.post(token_endpoint, data)

    def get_client(self):
        return self.client

    def set_registered(self, secret):
        self.registration_secret = secret

    def validate_tokens(self, access_code):
        response = self._post({
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': access_code,
            'redirect_uri': redirect_uri
        })
        response_data = json.loads(response.text)
        if response_data['access_token']:
            self.inject_token(response_data['access_token'])
        for i in response_data:
            print("key: ", i, "val: ", response_data[i])

    def inject_token(self, access_token):
        self.access_token = access_token
        if access_token == '':
            raise Exception('Access token was called with an empty string')

        self.client = spotipy.Spotify(auth=access_token)
        self.is_player_client = True
