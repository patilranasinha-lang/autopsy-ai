import pytest
from app import db
from app.models.sessions import BehaviorSession
from datetime import datetime, timedelta
from app.session_detection import SESSION_TYPES

@pytest.fixture
def auth_token(client):
    client.post('/api/auth/register', json={
        'username': 'sessionuser',
        'email': 'session@example.com',
        'password': 'password123'
    })
    resp = client.post('/api/auth/login', json={
        'email': 'session@example.com',
        'password': 'password123'
    })
    return resp.get_json()['access_token']

def test_generate_sessions_api(client, app, auth_token):
    response = client.post('/api/sessions/generate', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 201
    assert 'count' in response.json

def test_get_sessions_api(client, app, auth_token):
    with app.app_context():
        session = BehaviorSession(
            user_id=1,
            upload_id=1,
            session_type=SESSION_TYPES["DEEP_WORK"],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(minutes=60),
            duration_minutes=60.0,
            event_count=30,
            productivity_score=100.0
        )
        db.session.add(session)
        db.session.commit()

    response = client.get('/api/sessions', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert response.json['total'] >= 1
    assert len(response.json['sessions']) > 0

def test_get_session_summary_api(client, app, auth_token):
    response = client.get('/api/sessions/summary', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert 'total_sessions' in response.json
    assert 'deep_work_hours' in response.json
