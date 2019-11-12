from flask import request, jsonify, Response, redirect
from project.routes import routes
from project.services.spotify import init_search_service, PlayerService, build_auth_uri
import functools
import json

SpotifyService = PlayerService(init_search_service())
spotify_client = SpotifyService.client

def map_response_item(item):
    return {
        'track': item['name'],
        'artist': ', '.join(list(map(
            lambda x: x['name'],
            item['artists']
            ))),
        'id': item['id']
    }

@routes.route('/v1/spotify/search')
def search():
    search_string = request.args.get('query', '')
    if search_string == '':
        return 'Empty search string'
    result = spotify_client.search(search_string, type='track', limit=20)
    return jsonify(list(map(lambda a: map_response_item(a), result['tracks']['items'])))

@routes.route('/v1/spotify/now_playing')
def now_playing():
    if not SpotifyService.is_player_client:
        return 'Client not configured for user'
    print('Spotify accessToken is', SpotifyService.access_token)
    response = spotify_client.current_user()
    return response

@routes.route('/v1/spotify/auth')
def authenticate():
    if SpotifyService.registration_secret == '':
        generated_secret = 'Secret_Token'
        SpotifyService.set_registered(generated_secret) # Replace secret token with generated one.
        return redirect(build_auth_uri(generated_secret), code=302)
    auth_code = request.args.get('code')
    spotify_client = SpotifyService.inject_token(auth_code)
    return f'Authentication done with code {auth_code}'
