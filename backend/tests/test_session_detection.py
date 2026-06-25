import pytest
from datetime import datetime, timedelta
from app import db
from app.models.events import BehaviorEvent
from app.session_detection import SessionDetector, SESSION_TYPES

def test_session_detector_deep_work(app):
    with app.app_context():
        # Setup test data
        events = []
        base_time = datetime(2026, 1, 1, 9, 0, 0)
        
        for i in range(25): # 25 minutes of development
            events.append(BehaviorEvent(
                user_id=1,
                upload_id=1,
                timestamp=base_time + timedelta(minutes=i),
                category='development',
                event_type='active'
            ))

        detector = SessionDetector()
        sessions = detector.detect_sessions(events)
        
        assert len(sessions) == 1
        assert sessions[0].session_type == SESSION_TYPES["DEEP_WORK"]
        assert sessions[0].duration_minutes == 24.0
        assert sessions[0].event_count == 25

def test_session_detector_context_switching(app):
    with app.app_context():
        events = []
        base_time = datetime(2026, 1, 1, 9, 0, 0)
        
        categories = ['learning', 'entertainment', 'music', 'social']
        for i in range(10): 
            events.append(BehaviorEvent(
                user_id=1,
                upload_id=1,
                timestamp=base_time + timedelta(minutes=i),
                category=categories[i % 4],
                event_type='active'
            ))

        detector = SessionDetector()
        sessions = detector.detect_sessions(events)
        
        assert len(sessions) == 1
        assert sessions[0].session_type == SESSION_TYPES["CONTEXT_SWITCHING"]

def test_session_gap_split(app):
    with app.app_context():
        events = []
        base_time = datetime(2026, 1, 1, 9, 0, 0)
        
        # Session 1
        for i in range(5): 
            events.append(BehaviorEvent(
                user_id=1, upload_id=1, timestamp=base_time + timedelta(minutes=i),
                category='entertainment', event_type='active'
            ))
            
        # Gap > 15 mins
        # Session 2
        for i in range(5): 
            events.append(BehaviorEvent(
                user_id=1, upload_id=1, timestamp=base_time + timedelta(minutes=30+i),
                category='development', event_type='active'
            ))

        detector = SessionDetector(gap_threshold_minutes=15)
        sessions = detector.detect_sessions(events)
        
        assert len(sessions) == 2
        assert sessions[0].session_type == SESSION_TYPES["ENTERTAINMENT"]
        assert sessions[1].session_type == SESSION_TYPES["CODING"]
