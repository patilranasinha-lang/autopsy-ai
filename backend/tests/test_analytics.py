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
    assert data['category_distribution']['total_events'] == 0
    assert len(data['activity_over_time']['timeline']) == 0

def test_analytics_summary_with_data(client, auth_token, app):
    # Insert some dummy events
    with app.app_context():
        # Get user id (it should be 1 because it's an isolated test, but let's query it safely if needed. 
        # Actually in pytest with fresh db, the registered user is id=1)
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
    dist = data['category_distribution']
    assert dist['total_events'] == 3
    assert dist['distribution']['development'] == 2
    assert dist['distribution']['music'] == 1
    
    timeline = data['activity_over_time']['timeline']
    assert len(timeline) == 2 # 2 days
    assert timeline[0]['date'] == '2026-06-24'
    assert timeline[0]['count'] == 2
    assert timeline[1]['date'] == '2026-06-25'
    assert timeline[1]['count'] == 1
