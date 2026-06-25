import pytest
from app import db
from app.models.events import BehaviorEvent
from datetime import datetime

@pytest.fixture
def auth_token(client):
    client.post('/api/auth/register', json={
        'username': 'analyticsuser',
        'email': 'analytics@example.com',
        'password': 'password123'
    })
    resp = client.post('/api/auth/login', json={
        'email': 'analytics@example.com',
        'password': 'password123'
    })
    return resp.get_json()['access_token']

def test_analytics_summary_empty(client, auth_token):
    resp = client.get('/api/analytics/summary', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['categories_percentage'] == {}

def test_analytics_summary_with_data(client, auth_token, app):
    # Insert some dummy events
    with app.app_context():
        event1 = BehaviorEvent(user_id=1, upload_id=1, timestamp=datetime(2026, 6, 24, 10, 0, 0), source='chrome', event_type='visit', category='development', value='x')
        event2 = BehaviorEvent(user_id=1, upload_id=1, timestamp=datetime(2026, 6, 24, 11, 0, 0), source='chrome', event_type='visit', category='development', value='y')
        event3 = BehaviorEvent(user_id=1, upload_id=1, timestamp=datetime(2026, 6, 25, 10, 0, 0), source='spotify', event_type='play', category='music', value='z')
        db.session.add_all([event1, event2, event3])
        db.session.commit()

    resp = client.get('/api/analytics/summary', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    data = resp.get_json()
    
    assert resp.status_code == 200
    assert data['average_daily_activity'] == 1.5
    assert 'development' in data['categories_percentage']
    assert 'music' in data['categories_percentage']
