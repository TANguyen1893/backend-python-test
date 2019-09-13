import pytest
from test.test_utils import initialize_client

@pytest.fixture
def client():
    return initialize_client()

def login(client):
    client.post('/login', data=dict(
        username='user1',
        password='user1',
    ))

def test_not_logged_in(client):
    resp = client.post('/todo/', data=dict(description="abc"))
    assert 'http://localhost/login' == resp.headers['Location']
    assert resp.status_code == 302

def test_blank_description(client):
    login(client)
    resp = client.post('/todo/', data=dict(description=''))
    assert resp.status_code == 400

def test_valid_todo(client):
    login(client)
    todo = {
        'complete': 0,
        'description': 'my todo',
        'user_id': 1,
        'id': 80
    }
    resp = client.post('/todo/', data=todo)
    assert resp.status_code == 302

