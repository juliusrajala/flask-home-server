import os
import spotipy
import spotipy.oauth2 as spoAuth2
import json
import requests
from flask import (current_app as app)

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
        # '&show_dialog=true'
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
        self._last_active_device = ''

        self.client = client

    def _auth_headers(self):
        return {'Authorization': 'Bearer {0}'.format(self._access_token)}

    # HTTP_METHODS
    def _post_auth(self, data):
        return requests.post(token_endpoint, data)

    def _post(self, url, data={}):
        return requests.post(f'https://api.spotify.com/v1/{url}', headers=self._auth_headers(), data=data)

    def _put(self, url, data={}):
        app.logger.info(f'Put request with data {data}')
        return requests.put(f'https://api.spotify.com/v1/{url}?device_id={self._last_active_device}', headers=self._auth_headers(), json=data)

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

    def get_active_device(self):
        devices = self.devices()['devices']
        active_devices = list(
            filter(lambda x: x['is_active'] == True, devices))
        if len(active_devices) == 1:
            self._last_active_device = active_devices[0]['id']
            return
        if len(devices) > 1:
            self._last_active_device = devices[0]['id']

    # Authentication
    def set_registered(self, secret):
        self._registration_secret = secret

    def validate_tokens(self, access_code):
        response = self._post_auth({
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': access_code,
            'redirect_uri': redirect_uri
        })
        response_data = json.loads(response.text)
        if response_data['access_token']:
            self.inject_token(response_data['access_token'])
            app.logger.info(f'response from validation {response_data}')

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

    def currently_playing(self):
        uri = 'me/player'
        response = self._get(uri)
        return json.loads(response.text)

    def control_playback(self, command, uuid=''):
        """
            Following the documentation for the Spotify controls
            the player library returns a status-code of 204 on
            success, requests should be validated on route side
        """
        command_dict = {
            'next': self.play_next,
            'previous': self.play_previous,
            'play': self.play_pause
        }
        if command not in command_dict:
            return False

        if command == 'play':
            status = self.play_pause(uuid)
            return status == 204

        status = command_dict[command]()
        return status == 204

    def play_next(self):
        uri = 'me/player/next'
        response = self._post(uri)
        return response.status_code

    def play_previous(self):
        uri = 'me/player/previous'
        response = self._post(uri)
        return response.status_code

    def play_pause(self, uuid):
        uri = 'me/player/play'
        data = {}
        if uuid:
            track_id = f'spotify:track:{uuid}'
            data = {'uris': [track_id]}
        response = self._put(uri, data)
        app.logger.info(
            f'Request with {data} Responded with status {response}')
        return response.status_code
