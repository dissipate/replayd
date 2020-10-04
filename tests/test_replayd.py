import sys
sys.path.append('..')

import pytest
from http import HTTPStatus
from replayd import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_post(client):
    response_post = client.post('/', data='foo')
    response_get = client.get('/')
    print(dir(response_get))
    print(response_get.data)
    assert response_post.status_code == HTTPStatus.NO_CONTENT and response_get.data == b'foo'
