from flask import request, jsonify
from project.routes import routes

tracks = [
    { "track":"Test 1", "artist":"Artist", "id":"ID1" },
    { "track":"Test 2", "artist":"Artist", "id":"ID2" },
    { "track":"Test 3", "artist":"Artist", "id":"ID3" },
]

@routes.route('/v1/spotify/search')
def search():
    return jsonify(tracks)

@routes.route('/v1/spotify/now_playing')
def now_playing():
    return jsonify({ "track":"Test 4", "artist":"Artist", "id":"ID4" })