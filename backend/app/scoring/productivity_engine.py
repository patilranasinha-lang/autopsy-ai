from typing import List, Dict
from app.models.sessions import BehaviorSession
from app.session_detection import SESSION_TYPES
from .scoring_rules import BaseScoringEngine, normalize_score
from .scoring_config import SCORING_WEIGHTS, THRESHOLDS
from .focus_engine import FocusEngine
from .consistency_engine import ConsistencyEngine
from .discipline_engine import DisciplineEngine

class ProductivityEngine(BaseScoringEngine):
    def __init__(self):
        self.focus_engine = FocusEngine()
        self.consistency_engine = ConsistencyEngine()
        self.discipline_engine = DisciplineEngine()

    def calculate(self, daily_sessions: List[BehaviorSession], historical_sessions: List[BehaviorSession] = None) -> Dict[str, float]:
        if not daily_sessions:
            return {
                "productivity_score": 0.0,
                "focus_score": 0.0,
                "consistency_score": 0.0,
                "discipline_score": 0.0,
                "deep_work_score": 0.0
            }

        focus = self.focus_engine.calculate(daily_sessions, historical_sessions)
        consistency = self.consistency_engine.calculate(daily_sessions, historical_sessions)
        discipline = self.discipline_engine.calculate(daily_sessions, historical_sessions)
        
        # Calculate Deep Work sub-score based on threshold
        deep_work_mins = sum(s.duration_minutes for s in daily_sessions if s.session_type == SESSION_TYPES["DEEP_WORK"])
        deep_work = normalize_score((deep_work_mins / THRESHOLDS["IDEAL_DEEP_WORK_MINUTES"]) * 100.0)

        # Final weighted score
        final_score = (
            (deep_work * SCORING_WEIGHTS["DEEP_WORK_WEIGHT"]) +
            (focus * SCORING_WEIGHTS["FOCUS_WEIGHT"]) +
            (consistency * SCORING_WEIGHTS["CONSISTENCY_WEIGHT"]) +
            (discipline * SCORING_WEIGHTS["DISCIPLINE_WEIGHT"])
        )
        
        return {
            "productivity_score": normalize_score(final_score),
            "focus_score": focus,
            "consistency_score": consistency,
            "discipline_score": discipline,
            "deep_work_score": deep_work
        }
