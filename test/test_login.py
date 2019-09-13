import pytest
from passlib.hash import bcrypt
from test.test_utils import initialize_client
from main import create_hashed_salted_password

@pytest.fixture
def client():
    return initialize_client()

def test_blank_username_password(client):
    resp = client.post('/login', data=dict(
        username='',
        password='',
    ))
    assert 'http://localhost/login' == resp.headers['Location']
    assert resp.status_code == 302

def test_valid_user_name_password(client):
    resp = client.post('/login', data=dict(
        username='user1',
        password='user1',
    ))
    assert 'http://localhost/todo' == resp.headers['Location']
    assert resp.status_code == 302

def test_invalid_user_name(client):
    resp = client.post('/login', data=dict(
        username='abc',
        password='user2',
    ))
    assert 'http://localhost/login' == resp.headers['Location']
    assert resp.status_code == 302

def test_invalid_password(client):
    resp = client.post('/login', data=dict(
        username='user1',
        password='ABCDEFGH',
    ))
    assert 'http://localhost/login' == resp.headers['Location']
    assert resp.status_code == 302

def test_encrypt_password():
    password = 'user1'
    hashed_password = create_hashed_salted_password(password)
    assert bcrypt.verify(password, hashed_password) == True
