from typing import List
from app.models.sessions import BehaviorSession
from app.session_detection import SESSION_TYPES
from .scoring_rules import BaseScoringEngine, normalize_score
from .scoring_config import PENALTIES, THRESHOLDS

class DisciplineEngine(BaseScoringEngine):
    def calculate(self, daily_sessions: List[BehaviorSession], historical_sessions: List[BehaviorSession] = None) -> float:
        if not daily_sessions:
            return 0.0
            
        base_score = 100.0
        
        # Total durations
        entertainment_mins = sum(s.duration_minutes for s in daily_sessions if s.session_type == SESSION_TYPES["ENTERTAINMENT"])
        work_mins = sum(s.duration_minutes for s in daily_sessions if s.session_type in [SESSION_TYPES["DEEP_WORK"], SESSION_TYPES["CODING"], SESSION_TYPES["STUDY"]])
        
        # Penalty for excess entertainment
        if entertainment_mins > THRESHOLDS["ACCEPTABLE_ENTERTAINMENT_MINUTES"]:
            excess_mins = entertainment_mins - THRESHOLDS["ACCEPTABLE_ENTERTAINMENT_MINUTES"]
            penalty = excess_mins * abs(PENALTIES["ENTERTAINMENT_PENALTY"])
            base_score -= penalty
            
        # Bonus for high work ratio
        total_mins = sum(s.duration_minutes for s in daily_sessions)
        if total_mins > 0:
            work_ratio = work_mins / total_mins
            if work_ratio > 0.5:
                base_score += (work_ratio - 0.5) * 40.0 # Up to 20 bonus points
                
        return normalize_score(base_score)
