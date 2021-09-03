import unittest.mock as mock

import pytest

from app import create_app


DUMMY_API_RESULT = {
    'number_of_platforms': 1,
    'name': ['pokemon'],
    'aliases': ['pokemans']}


@pytest.fixture
def client():
    app = create_app('testing')
    # mock up the giantbomb client
    app.giant_bomb_client = mock.Mock(
        search=mock.Mock(return_value=DUMMY_API_RESULT))
    with app.test_client() as client:
        yield client


def test_videogame_search(client):
    # sending a request without a "term" param should result in a 406
    rv = client.get('/videogames/search')
    assert rv.status_code == 406, f'{rv.status_code} != 406'
    assert rv.json.get('detail') is not None, f'{rv.json.get("detail")} is None.'
    # sending a valid "term" should result in a successful response
    rv = client.get('/videogames/search?term=rocket')
    assert rv.status_code == 200, f'{rv.status_code} != 200'
    assert rv.json == DUMMY_API_RESULT, f'{rv.json} != {DUMMY_API_RESULT}'


def test_not_found(client):
    rv = client.get('/something/search')
    assert rv.status_code == 404, f'{rv.status_code} != 404'
    rv = client.get('/')
    assert rv.status_code == 404, f'{rv.status_code} != 404'
    rv = client.get('/videogames')
    assert rv.status_code == 404, f'{rv.status_code} != 404'