import pytest
from app.models import User


def test_create_user(client, app):
    """Test creating a new user via API"""
    response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data
    assert 'password_hash' not in data


def test_create_user_duplicate_username(client, app):
    """Test creating user with duplicate username"""
    # Create first user
    client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'testpass123'
        }
    )
    
    # Try to create duplicate username
    response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'testpass123'
        }
    )
    assert response.status_code == 400


def test_get_users(client, app):
    """Test getting paginated list of users"""
    # Create multiple users
    for i in range(5):
        client.post(
            '/api/users',
            json={
                'username': f'user{i}',
                'email': f'user{i}@example.com',
                'password': 'testpass123'
            }
        )
    
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data
    assert 'page' in data
    assert 'per_page' in data
    assert len(data['items']) == 5


def test_get_user_by_id(client, app):
    """Test getting a single user by ID"""
    # Create user first
    create_response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    )
    user_id = create_response.get_json()['id']
    
    # Get user by ID
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == user_id
    assert data['username'] == 'testuser'


def test_get_nonexistent_user(client, app):
    """Test getting a user that doesn't exist"""
    response = client.get('/api/users/9999')
    assert response.status_code == 404
