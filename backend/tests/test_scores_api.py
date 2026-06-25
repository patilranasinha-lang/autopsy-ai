import json
from datetime import datetime
from app.models.scores import ProductivityScore
from app import db

def test_generate_scores_api(client, auth_headers, test_user):
    # Post to generate scores
    response = client.post('/api/scores/generate', headers=auth_headers)
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert "score" in data
    assert data["score"]["productivity_score"] >= 0

def test_get_today_scores(client, auth_headers, test_user):
    # Setup score
    score = ProductivityScore(user_id=test_user.id, date=datetime.utcnow().date(), productivity_score=85.0)
    with client.application.app_context():
        db.session.add(score)
        db.session.commit()
        
    response = client.get('/api/scores/today', headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert "scores" in data
    assert data["scores"]["productivity_score"] == 85.0
    assert "insights" in data

def test_get_trends(client, auth_headers, test_user):
    response = client.get('/api/scores/trends', headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert "current_week_avg" in data
