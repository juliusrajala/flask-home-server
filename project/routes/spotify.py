from flask import request, jsonify, Response
from project.routes import routes
from project.services.spotify import init_service
import functools
import json

spotify_client = init_service()

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
    return jsonify({ "track":"Test 4", "artist":"Artist", "id":"ID4" })