import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


class TestAuthEndpoints:
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'User registered successfully'
        assert data['data']['user']['username'] == 'testuser'
        assert data['data']['user']['email'] == 'test@example.com'
        assert 'password' not in data['data']['user']
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'password': 'testpassword123'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'required' in data['message'].lower()
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        # First registration
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'testpassword123'
        })
        # Second registration with same username
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'testpassword123'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'already exists' in data['message']
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # First registration
        client.post('/api/auth/register', json={
            'username': 'testuser1',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        # Second registration with same email
        response = client.post('/api/auth/register', json={
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'already exists' in data['message']
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'testpassword123'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'invalid email' in data['message'].lower()
    
    def test_register_short_password(self, client):
        """Test registration with too short password"""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'password must be at least 8' in data['message'].lower()
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register first
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        # Login
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Login successful'
        assert 'access_token' in data['data']
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        # Register first
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        # Login with wrong password
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert data['message'] == 'Invalid credentials'
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user (should return same generic error)"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'anypassword'
        })
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert data['message'] == 'Invalid credentials'
    
    def test_profile_unauthorized(self, client):
        """Test accessing profile without authentication"""
        response = client.get('/api/auth/profile/1')
        assert response.status_code == 401
    
    def test_profile_authorized(self, client):
        """Test accessing profile with valid authentication"""
        # Register and login
        register_response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        user_id = register_response.get_json()['data']['user']['id']
        
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        access_token = login_response.get_json()['data']['access_token']
        
        # Get profile
        response = client.get(f'/api/auth/profile/{user_id}', headers={
            'Authorization': f'Bearer {access_token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['user']['username'] == 'testuser'
