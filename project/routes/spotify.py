from flask import request, jsonify, Response
from project.routes import routes
from project.services.spotify import init_search_service, PlayerService
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
        print("Faulty query")
        return 'Bad query'
    result = spotify_client.search(search_string, type='track', limit=20)
    return jsonify(list(map(lambda a: map_response_item(a), result['tracks']['items'])))

@routes.route('/v1/spotify/now_playing')
def now_playing():
    if not SpotifyService.is_player_client:
        return 'Client not configured for user'
    response = spotify_client.current_user()
    return response

@routes.route('/v1/spotify/auth')
def authenticate():
    global spotify_client
    auth_code = request.args.get('code')
    spotify_client = SpotifyService.inject_token(auth_code)
    return f'Registered token {auth_code}'
