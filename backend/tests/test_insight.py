import pytest
from app.services.insight_service import InsightService
from app.models.events import BehaviorEvent
from app import db
from datetime import datetime

def test_generate_insights_empty(app, client):
    with app.app_context():
        insights = InsightService.generate_insights(1)
        assert len(insights) > 0
        assert insights[0]['type'] == 'info'

def test_generate_insights_with_data(app, client):
    with app.app_context():
        event1 = BehaviorEvent(
            user_id=1,
            upload_id=1,
            timestamp=datetime.utcnow(),
            source="chrome",
            event_type="visit",
            category="learning"
        )
        db.session.add(event1)
        db.session.commit()

        insights = InsightService.generate_insights(1)
        assert len(insights) > 0
        # Ensure we have some insights now
        assert any(i['type'] != 'info' for i in insights)
