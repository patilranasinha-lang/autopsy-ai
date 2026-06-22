import pytest


def test_create_report(client, app):
    """Test creating a new report via API"""
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
    
    # Create a report
    response = client.post(
        '/api/reports',
        json={
            'user_id': user_id,
            'report_type': 'analysis',
            'report_data': {'insights': 'test data', 'summary': 'test summary'}
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['report_type'] == 'analysis'
    assert data['user_id'] == user_id
    assert 'report_data' in data


def test_get_reports(client, app):
    """Test getting paginated list of reports"""
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
    
    # Create multiple reports
    for i in range(4):
        client.post(
            '/api/reports',
            json={
                'user_id': user_id,
                'report_type': f'type{i}',
                'report_data': {'data': f'report{i}'}
            }
        )
    
    # Get all reports
    response = client.get('/api/reports')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 4
    
    # Get reports by user ID
    response = client.get(f'/api/reports?user_id={user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 4


def test_get_report_by_id(client, app):
    """Test getting a single report by ID"""
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
    
    # Create a report
    report_response = client.post(
        '/api/reports',
        json={
            'user_id': user_id,
            'report_type': 'analysis',
            'report_data': {'key': 'value'}
        }
    )
    report_id = report_response.get_json()['id']
    
    # Get report by ID
    response = client.get(f'/api/reports/{report_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == report_id


def test_get_nonexistent_report(client, app):
    """Test getting a report that doesn't exist"""
    response = client.get('/api/reports/9999')
    assert response.status_code == 404
