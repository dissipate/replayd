from flask import Flask, request, make_response, jsonify
from flask_caching import Cache
from http import HTTPStatus
import sys
import toml
import os

def configure_app(app):
    config_path = os.environ.get('REPLAYD_CONFIG_PATH')

    if config_path is None:
        path = os.path.abspath(os.path.join(os.path.abspath(os.sep), 'etc', 'replayd', 'config.toml'))
        config = toml.load(path)
    else:
        config = toml.load(config_path)

    app.config.from_mapping(config)

app = Flask(__name__)
configure_app(app)

CACHE_KEY_FMT = "{}_{}".format
CACHE_DATA_KEY = CACHE_KEY_FMT(__name__, "post_put")
CACHE_CONTENT_TYPE_KEY = CACHE_KEY_FMT(__name__, "content_type")

PAYLOAD_TOO_LARGE_MSG_FMT = "Payload too large, payload cannot exceed {} bytes\n".format
NOT_FOUND_MSG = 'Data not found, must POST to / first'
FIVE_HUNDRED_MSG = 'Oops, something has gone wrong'

@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return FIVE_HUNDRED_MSG, HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/', methods=['POST', 'PUT'])
def set_data():

    MAX_LENGTH = app.config['MAX_CONTENT_LENGTH']

    if request.content_length > MAX_LENGTH:
        PAYLOAD_TOO_LARGE_MSG = PAYLOAD_TOO_LARGE_MSG_FMT(MAX_LENGTH)
        return PAYLOAD_TOO_LARGE_MSG, HTTPStatus.REQUEST_ENTITY_TOO_LARGE

    cache = Cache(app)
    cache.set(CACHE_DATA_KEY, request.get_data())
    cache.set(CACHE_CONTENT_TYPE_KEY, request.content_type)

    return '', HTTPStatus.NO_CONTENT

@app.route('/', methods=['GET'])
def get_data():
    cache = Cache(app)
    cached_data = cache.get(CACHE_DATA_KEY)
    cached_content_type = cache.get(CACHE_CONTENT_TYPE_KEY)

    if cached_data is None:
        return NOT_FOUND_MSG, HTTPStatus.NOT_FOUND

    return cached_data, HTTPStatus.OK, {'Content-Type': cached_content_type}

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
