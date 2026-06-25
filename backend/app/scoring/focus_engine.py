from typing import List
from app.models.sessions import BehaviorSession
from app.session_detection import SESSION_TYPES
from .scoring_rules import BaseScoringEngine, normalize_score
from .scoring_config import PENALTIES

class FocusEngine(BaseScoringEngine):
    def calculate(self, daily_sessions: List[BehaviorSession], historical_sessions: List[BehaviorSession] = None) -> float:
        if not daily_sessions:
            return 0.0
            
        base_score = 100.0
        
        # Calculate penalties for context switching
        switch_sessions = [s for s in daily_sessions if s.session_type == SESSION_TYPES["CONTEXT_SWITCHING"]]
        total_switches = sum(s.event_count for s in switch_sessions)
        
        switch_penalty = total_switches * abs(PENALTIES["CONTEXT_SWITCH"])
        
        # Reward longer average duration
        avg_duration = sum(s.duration_minutes for s in daily_sessions) / len(daily_sessions)
        duration_bonus = min(20.0, avg_duration / 5.0) # Cap at 20 points bonus
        
        final_score = base_score - switch_penalty + duration_bonus
        return normalize_score(final_score)
