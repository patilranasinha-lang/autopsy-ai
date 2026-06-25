import pytest
from app.services.timeline_service import TimelineService
from app.models.events import BehaviorEvent
from app import db
from datetime import datetime, timedelta

def test_get_timeline_daily(app, client):
    with app.app_context():
        # Setup test data
        event1 = BehaviorEvent(
            user_id=1,
            upload_id=1,
            timestamp=datetime.utcnow() - timedelta(days=1),
            source="chrome",
            event_type="visit",
            category="learning"
        )
        event2 = BehaviorEvent(
            user_id=1,
            upload_id=1,
            timestamp=datetime.utcnow() - timedelta(days=1),
            source="chrome",
            event_type="visit",
            category="entertainment"
        )
        db.session.add_all([event1, event2])
        db.session.commit()

        # Run test
        result = TimelineService.get_timeline(1, period='daily')
        
        assert result['period'] == 'daily'
        assert len(result['timeline']) > 0
        assert result['timeline'][0]['count'] >= 2
