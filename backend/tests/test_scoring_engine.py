from datetime import datetime, timedelta
from app.session_detection import SESSION_TYPES
from app.models.sessions import BehaviorSession
from app.scoring.focus_engine import FocusEngine
from app.scoring.discipline_engine import DisciplineEngine
from app.scoring.scoring_rules import normalize_score

def test_normalize_score():
    assert normalize_score(150.0) == 100.0
    assert normalize_score(-50.0) == 0.0
    assert normalize_score(50.555) == 50.56

def test_focus_engine_penalties():
    engine = FocusEngine()
    base_time = datetime(2026, 1, 1, 9, 0, 0)
    
    # 5 switches
    sessions = [
        BehaviorSession(
            session_type=SESSION_TYPES["CONTEXT_SWITCHING"],
            duration_minutes=20,
            event_count=5,
            start_time=base_time
        )
    ]
    
    score = engine.calculate(sessions)
    # Penalty: 5 * 2.0 = 10. Base 100 - 10 + duration_bonus (20 / 5 = 4) = 94.0
    assert score == 94.0

def test_discipline_engine_penalties():
    engine = DisciplineEngine()
    base_time = datetime(2026, 1, 1, 9, 0, 0)
    
    sessions = [
        BehaviorSession(
            session_type=SESSION_TYPES["ENTERTAINMENT"],
            duration_minutes=120, # 60 over threshold
            event_count=10,
            start_time=base_time
        )
    ]
    
    score = engine.calculate(sessions)
    # Base 100 - (60 * 0.5) = 70.0
    assert score == 70.0
