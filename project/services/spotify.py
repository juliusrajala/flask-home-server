import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def init_service():
    client_id = str(os.environ.get("SPOTIFY_CLIENT_ID", ''))
    client_secret = str(os.environ.get("SPOTIFY_CLIENT_SECRET", ''))
    if client_id == '' or client_secret == '':
        raise Exception('Invalid spotify authorization')
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(client_credentials_manager=credentials_manager)
    return spotipy_client