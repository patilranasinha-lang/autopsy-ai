import pytest
from app import create_app, db
from app.models.core import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(username='test_user', email='test@test.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def token(client):
    with client.application.app_context():
        user = User.query.first()
        return create_access_token(identity=str(user.id))

def test_generate_burnout_assessment(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    res = client.post('/api/burnout/generate', headers=headers)
    assert res.status_code == 200
    assert 'assessment' in res.json
    assert res.json['assessment']['risk_level'] == 'Low' # Since there's no data

def test_get_history(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    res = client.get('/api/burnout/history', headers=headers)
    assert res.status_code == 200
    assert 'history' in res.json
