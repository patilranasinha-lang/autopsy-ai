import pytest


def test_create_upload(client, app):
    """Test creating a new upload via API"""
    # First create a user
    user_response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    )
    user_id = user_response.get_json()['id']
    
    # Create an upload
    response = client.post(
        '/api/uploads',
        json={
            'user_id': user_id,
            'file_name': 'test.csv',
            'file_type': 'text/csv',
            'file_size': 1024
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['file_name'] == 'test.csv'
    assert data['user_id'] == user_id
    assert data['processing_status'] == 'pending'


def test_get_uploads(client, app):
    """Test getting paginated list of uploads"""
    # First create a user
    user_response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    )
    user_id = user_response.get_json()['id']
    
    # Create multiple uploads
    for i in range(3):
        client.post(
            '/api/uploads',
            json={
                'user_id': user_id,
                'file_name': f'test{i}.csv',
                'file_type': 'text/csv',
                'file_size': 1024
            }
        )
    
    # Get all uploads
    response = client.get('/api/uploads')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 3
    
    # Get uploads by user ID
    response = client.get(f'/api/uploads?user_id={user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 3


def test_get_upload_by_id(client, app):
    """Test getting a single upload by ID"""
    # First create a user
    user_response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    )
    user_id = user_response.get_json()['id']
    
    # Create an upload
    upload_response = client.post(
        '/api/uploads',
        json={
            'user_id': user_id,
            'file_name': 'test.csv',
            'file_type': 'text/csv',
            'file_size': 1024
        }
    )
    upload_id = upload_response.get_json()['id']
    
    # Get upload by ID
    response = client.get(f'/api/uploads/{upload_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == upload_id


def test_get_nonexistent_upload(client, app):
    """Test getting an upload that doesn't exist"""
    response = client.get('/api/uploads/9999')
    assert response.status_code == 404
