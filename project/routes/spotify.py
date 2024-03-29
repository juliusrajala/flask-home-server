import functools
import time
import json
from flask import request, jsonify, Response, redirect, current_app
from project.routes import routes
from project.services.spotify import init_search_service, SpotifyService, build_auth_uri

spotifyService = SpotifyService(init_search_service())
spotify_client = spotifyService.get_client


def map_spotify_song(item):
    return {
        'track': item['name'],
        'artist': ', '.join(list(map(
            lambda x: x['name'],
            item['artists']
        ))),
        'album': item['album']['name'],
        'id': item['id']
    }


@routes.route('/v1/spotify/search')
def search():
    search_string = request.args.get('query', '')
    if search_string == '':
        return 'Empty search string'
    result = spotify_client().search(search_string, type='track', limit=20)
    return jsonify(list(map(lambda a: map_spotify_song(a), result['tracks']['items'])))


@routes.route('/v1/spotify/now_playing')
def now_playing():
    if not spotifyService.is_active():
        return 'Client not authorized yet'
    response = spotifyService.currently_playing()
    current_app.logger.info(response)
    return jsonify(map_spotify_song(response['item']))


@routes.route('/v1/spotify/devices')
def get_devices():
    return jsonify(spotifyService.devices())


@routes.route('/v1/spotify/control', methods=['POST', 'GET'])
def control_playback():
    if not spotifyService.is_active():
        return 'Client not authorized yet'

    if request.method == 'POST':
        json_data = request.get_json()
        command = json_data['command']
        current_app.logger.info(f'Parameters for playback {json_data}')
        if not command:
            return 'Bad request body, include command in request'
        if spotifyService.control_playback(command=command, uuid=json_data['uuid'] if 'uuid' in json_data else ''):
            # Sadly, it takes a bit to start the playback.
            # We make up for it with this nasty wait here.
            time.sleep(3)
            response = spotifyService.currently_playing()
            return jsonify(map_spotify_song(response['item']))

    response = spotifyService.currently_playing()
    return jsonify(map_spotify_song(response['item']))


@routes.route('/v1/spotify/auth')
def authenticate():
    if spotifyService.is_active():
        current_app.logger.info('Access token already found')
        return jsonify(spotify_client().current_user())

    if spotifyService.test_secret():  # We validate the source with a secret
        generated_secret = 'Secret_Token'
        # Replace temporary token with generated one.
        spotifyService.set_registered(generated_secret)
        return redirect(build_auth_uri(generated_secret), code=302)

    access_code = request.args.get('code')
    received_secret = request.args.get('state')
    if spotifyService.test_secret(received_secret) and access_code:
        spotifyService.validate_tokens(access_code)
        return f'Updating access tokens with {access_code}'

    raise Exception(
        f'Something went wrong {spotifyService.is_active()} {spotifyService._access_token}')
