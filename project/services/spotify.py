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


class SpotifyService:
    """Using the spotify authorization code flow. """

    def __init__(self, client):
        self._access_token = ''
        self._registration_secret = ''
        self._is_active_client = False

        self.client = client

    def _auth_headers(self):
        return {'Authorization': 'Bearer {0}'.format(self._access_token)}

    # HTTP_METHODS
    def _post(self, data):
        return requests.post(token_endpoint, data)

    def _get(self, url):
        return requests.get(f'https://api.spotify.com/v1/{url}', headers=self._auth_headers())

    # Service-utilities
    def test_secret(self, comparison=''):
        """
        :param: Comparison is empty by default
        """
        return self._registration_secret == comparison

    def is_active(self):
        return self._is_active_client and self._access_token != ''

    def get_client(self):
        return self.client

    # Authentication
    def set_registered(self, secret):
        self._registration_secret = secret

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

    def refresh_token(self):
        """ TODO: Implement refresh-token flow """

    def inject_token(self, access_token):
        if access_token == '':
            raise Exception('Access token was called with an empty string')

        self._access_token = access_token
        self.client = spotipy.Spotify(auth=access_token)
        self._is_active_client = True

    # API-endpoints
    def devices(self):
        uri = 'me/player/devices'
        response = self._get(uri)
        return json.loads(response.text)
