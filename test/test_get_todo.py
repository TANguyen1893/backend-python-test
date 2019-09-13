import pytest
from test.test_utils import initialize_client
from alayatodo.models.models import *
import json


@pytest.fixture
def client():
    return initialize_client()

def login(client):
    client.post('/login', data=dict(
        username='user1',
        password='user1',
    ))

def test_not_logged_in(client):
    resp = client.get('/todo/?page=1')
    assert 'http://localhost/login' == resp.headers['Location']
    assert resp.status_code == 302

def test_get_valid_todo(client):
    login(client)
    todo = {
        'complete': 0,
        'description': 'Vivamus tempus',
        'user_id': 1,
        'id': 1
    }
    resp = json.loads(client.get('/todo/1/json').data.decode('utf-8'))
    for d in resp:
        assert resp[d] == todo[d]

def test_get_invalid_todo(client):
    login(client)
    resp = json.loads(client.get('/todo/10001/json').data.decode('utf-8')) # 10001 shouldn't exist
    assert int(resp["code"]) == 404
