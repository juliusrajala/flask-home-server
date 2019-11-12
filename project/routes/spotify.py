from flask import request, jsonify, Response, redirect
from project.routes import routes
from project.services.spotify import init_search_service, PlayerService, build_auth_uri
import functools

SpotifyService = PlayerService(init_search_service())
spotify_client = SpotifyService.get_client


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
    result = spotify_client().search(search_string, type='track', limit=20)
    return jsonify(list(map(lambda a: map_response_item(a), result['tracks']['items'])))


@routes.route('/v1/spotify/now_playing')
def now_playing():
    if not SpotifyService.is_player_client:
        return 'Client not configured for user'
    print('Spotify accessToken is', SpotifyService.access_token)
    response = spotify_client().current_user()
    return response


@routes.route('/v1/spotify/auth')
def authenticate():
    if SpotifyService.registration_secret == '':
        generated_secret = 'Secret_Token'
        # Replace secret token with generated one.
        SpotifyService.set_registered(generated_secret)
        return redirect(build_auth_uri(generated_secret), code=302)
    access_code = request.args.get('code')

    if SpotifyService.access_token:
        print(f'Access token already found {access_code}')
        return jsonify(spotify_client().current_user())

    received_secret = request.args.get('state')

    if received_secret == SpotifyService.registration_secret and access_code:
        SpotifyService.validate_tokens(access_code)
        return f'Updating access tokens with {access_code}'

    raise Exception('Something went wrong')
